import flet as ft
from httpcore import URL
import requests
import qrcode
import os
from components import botao_home, get_storage, set_storage
from config import SUPABASE_URL, HEADERS

def wallet(page):
    set_storage(page, "current_page", "wallet")
    
    page.title = "Minha Carteira - Agenda de Eventos"
    page.bgcolor = "#E8E8E8"
    
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    

    email = get_storage(page, "email")
    if not email:
        from login import login
        page.clean()
        login(page)
        return

    def buscar_ingressos():
        user_id = get_storage(page, "user_id")
        # Este select busca o ingresso E os detalhes do evento vinculado
        URL = f"{SUPABASE_URL}/ingressos?user_id=eq.{user_id}&select=*,eventos_db(*)"
    
        try:
            response = requests.get(URL, headers=HEADERS)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erro ao buscar ingressos: {e}")
            return []

    ingressos = buscar_ingressos()

    def ver_qr_code(hash_val, titulo_evento):
        # 1. Gerar o QR Code com o hash do banco
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(hash_val)
        qr.make(fit=True)
    
        img = qr.make_image(fill_color="black", back_color="white")
    
        # 2. Salvar temporariamente
        path_img = os.path.join("assets", "temp_qr.png")
        img.save(path_img)
    
        # 3. Mostrar no Modal do Flet
        def fechar_modal(e):
            modal.open = False
            page.update()

        modal = ft.AlertDialog(
            title=ft.Text(f"Ingresso: {titulo_evento}"),
            content=ft.Column([
                ft.Image(src=path_img, width=200, height=200),
                ft.Text(hash_val, size=10, color="grey") # Mostra o hash em texto para conferência
            ], tight=True),
            actions=[ft.TextButton("Fechar", on_click=fechar_modal)],
        )
    
        page.overlay.append(modal)
        modal.open = True
        page.update()

    lista_ingressos = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    for ing in ingressos:
        # Extrai os dados do evento que vêm aninhados do Supabase
        ev = ing.get("eventos_db", {})
        
        # Pega a foto do dicionário do evento (ev)
        foto = ev.get("foto_evento")

        imagem_evento = ft.Container(
            content=ft.Image(
                src=foto if foto else "",
                width=80,
                height=80,
                fit="cover",
                border_radius=10,
            ) if foto else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=40, color="grey"),
            width=80,
            height=80,
            bgcolor="#f0f0f0",
            border_radius=10,
        )

        ver_qrcode = ft.ElevatedButton(
            content=ft.Text("Ver QR Code", size=12), 
            # 'h' vem do ingresso, 't' vem do evento
            on_click=lambda e, h=ing["qr_code_hash"], t=ev.get("titulo", "Evento"): ver_qr_code(h, t),
            bgcolor="#0D004E",
            color="white",
            style=ft.ButtonStyle(padding=10)
        )

        detalhes_img_evento = ft.Column(
            [
                ft.Text(ev.get("titulo", "Sem título"), weight="bold", size=16, color="#0D004E"),
                ft.Text(f"Data: {ev.get('data_evento', '')} {ev.get('hora_evento', '')}", size=12, color="grey"),
                ft.Text(f"Local: {ev.get('local_evento', '')}", size=12, color="grey"),
            ],
            expand=True,
            spacing=2
        )

        lista_ingressos.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        imagem_evento,
                        ft.VerticalDivider(width=10, color="transparent"),
                        detalhes_img_evento,
                        ver_qrcode
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor="white",
                padding=25,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, "black"))
            )
        )

    if not ingressos:
        lista_ingressos.controls.append(ft.Text("Você ainda não possui ingressos.", size=18, color="grey"))

    page.add(
        ft.Container(
            ft.Row(
                controls = [
                    ft.Image(src="assets/icons/logo_temporaria.png", width=35, height=35),
                    ft.Column(
                        [
                            ft.Text("Magnus", size=20, weight="bold", color="white"),
                            ft.Text("Minha Carteira", size=16, color="white"),
                        ],
                        alignment=ft.CrossAxisAlignment.START,
                        spacing=0
                    ),
                    ft.Container(expand=True),
                    botao_home(page)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            bgcolor="#0D004E",
            padding=25,
            border_radius=10,
        ),
        ft.Container(
            content=lista_ingressos,
            padding=20,
            expand=True
        )
    )
