import flet as ft
import requests
import qrcode
import os
import io
import base64
from components import botao_home, get_storage, set_storage
from config import SUPABASE_URL, HEADERS

def wallet(page):
    set_storage(page, "current_page", "wallet")
    
    page.title = "Minha Carteira - Agenda de Eventos"
    page.bgcolor = "#E8E8E8"
    page.scroll = ft.ScrollMode.ALWAYS 

    logado = get_storage(page, "logado")
    user_id = get_storage(page, "user_id")

    def ir_home(e=None):
        page.clean()
        from home import home 
        home(page)

    if not logado or not user_id:
        print("Sessão inválida na carteira. Redirecionando...")
        from login import login
        page.clean()
        login(page)
        return
    
    def validar_ingresso(ingresso_id):
        url_patch = f"{SUPABASE_URL}/ingressos?id=eq.{ingresso_id}"
    
        dados = {"usado": True}
    
        response = requests.patch(url_patch, json=dados, headers=HEADERS)
    
        if response.status_code in [200, 204]:
            print("Ingresso invalidado com sucesso! (Status: USADO)")
            return True
        return False
    

    def buscar_ingressos():
        endpoint = f"{SUPABASE_URL}/ingressos?user_id=eq.{user_id}&select=*,eventos_db(*)"
    
        try:
            response = requests.get(endpoint, headers=HEADERS)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erro ao buscar ingressos: {e}")
            return []

    ingressos = buscar_ingressos()

    def ver_qr_code(hash_val, titulo_evento):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(hash_val)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
    
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        def fechar_modal(e):
            modal.open = False
            page.update()

        modal = ft.AlertDialog(
            title=ft.Text(f"Ingresso: {titulo_evento}"),
            content=ft.Column([
                ft.Image(
                    src=f"data:image/png;base64,{img_base64}", 
                    width=200, 
                    height=200
                ),
                ft.Text(f"Código: {hash_val[:10]}...", size=12, color="grey")
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[ft.TextButton("Fechar", on_click=fechar_modal)],
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    # --- Construção da UI ---
    lista_ingressos = ft.Column(spacing=10, expand=True)
    
    for ing in ingressos:
        ev = ing.get("eventos_db", {})
        foto = ev.get("foto_evento")
        usado = ing.get("usado", False) 

        cor_fundo = "white" if not usado else "#f0f0f0"
        
        detalhes = ft.Column([
            ft.Text(ev.get("titulo", "Evento"), weight="bold", size=16, color="#0D004E"),
            ft.Text(f"Data: {ev.get('data_evento', '')}", size=12, color="grey"),
            ft.Text("INGRESSO JÁ UTILIZADO" if usado else "VÁLIDO", 
                    size=10, weight="bold", color="red" if usado else "green")
        ], expand=True, spacing=2)

        ver_btn = ft.ElevatedButton(
            "QR Code",
            icon=ft.Icons.QR_CODE,
            on_click=lambda e, h=ing["qr_code_hash"], t=ev.get("titulo"): ver_qr_code(h, t),
            bgcolor="#0D004E" if not usado else "grey",
            color="white",
            disabled=usado
        )

        lista_ingressos.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Image(src=foto if foto else "assets/icons/logo_temporaria.png", width=60, height=60, fit="cover", border_radius=5),
                    detalhes,
                    ver_btn
                ]),
                bgcolor=cor_fundo,
                padding=15,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color="black12")
            )
        )

    if not ingressos:
        page.clean()
        page.add(
            ft.Container(
                content=ft.Row([
                    ft.Image(src="icons/logo_temporaria.png", width=35, height=35), 
                    ft.Text("Minha Carteira", size=20, weight="bold", color="white"),
                    ft.Container(expand=True),
                    botao_home(page)
                ]),
                bgcolor="#0D004E",
                padding=20,
                border_radius=10,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CONFIRMATION_NUMBER_OUTLINED, size=64, color="grey"),
                    ft.Text("Sua carteira está vazia", size=20, color="grey", weight="bold"),
                    ft.Text("Compre ingressos na página inicial", color="grey"),
                    ft.ElevatedButton(
                        "Ver Eventos", 
                        icon=ft.Icons.HOME, 
                        on_click=ir_home
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=100,
                alignment=ft.alignment.Alignment(0, 0)
            )
        )
        return

    page.clean()
    page.add(
        ft.Container(
            content=ft.Row([
                ft.Image(src="assets/icons/logo_temporaria.png", width=35, height=35),
                ft.Text("Minha Carteira", size=20, weight="bold", color="white"),
                ft.Container(expand=True),
                botao_home(page)
            ]),
            bgcolor="#0D004E",
            padding=20,
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
        ),
        ft.Container(content=lista_ingressos, padding=20)
    )