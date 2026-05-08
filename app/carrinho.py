import flet as ft
from httpcore import URL
import requests
from components import botao_home, get_storage, set_storage
from config import SUPABASE_URL, HEADERS
import uuid

def carrinho(page):
    set_storage(page, "current_page", "carrinho")
    page.title = "Meu Carrinho - Agenda de Eventos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#E8E8E8"

    cart = get_storage(page, "cart") or []

    def remover_item(item):
        cart.remove(item)
        set_storage(page, "cart", cart)
        page.clean()
        carrinho(page)

    def processar_compra(metodo_pagamento):
        user_id = get_storage(page, "user_id")
        URL_INGRESSOS = f"{SUPABASE_URL}/ingressos"
        
        try:
            for item in cart:
                sufixo = uuid.uuid4().hex[:6] 
                dados = {
                    "user_id": user_id,
                    "evento_id": item["id"],
                    "qr_code_hash": f"PASS_{user_id}_{item['id']}_{sufixo}" 
                }
                requests.post(URL_INGRESSOS, json=dados, headers=HEADERS)
            
            set_storage(page, "cart", [])
            
            def fechar_sucesso(e):
                sucesso_chamada.open = False
                page.update()
                page.clean()
                from home import home
                home(page)

            sucesso_chamada = ft.AlertDialog(
                bgcolor="#0D004E",
                title=ft.Text("Pagamento Aprovado!", color="white", weight="bold"),
                content=ft.Column(
                    [
                        ft.Text(f"Sua compra via {metodo_pagamento} foi confirmada!", color="white", text_align=ft.TextAlign.CENTER),
                        ft.Text("Os ingressos já estão na sua carteira.", size=12, color="white70", text_align=ft.TextAlign.CENTER),
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    tight=True, 
                    spacing=15
                ),
                actions=[
                    ft.ElevatedButton(
                        "Ir para Home", 
                        on_click=fechar_sucesso,
                        bgcolor="white",
                        color="#0D004E",
                        style=ft.ButtonStyle(text_style=ft.TextStyle(weight="bold"))
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            page.overlay.append(sucesso_chamada)
            sucesso_chamada.open = True
            page.update()

        except Exception as err:
            print("Erro na requisição:", err)
            page.overlay.append(ft.SnackBar(ft.Text("Erro ao processar compra."), open=True))
            page.update()

    def abrir_pagamento(e):
        logado = get_storage(page, "logado")
        
        if not logado:
            from login import login
            page.clean()
            login(page)
            page.overlay.append(ft.SnackBar(ft.Text("Você precisa estar logado para finalizar a compra!"), open=True))
            page.update()
            return

        def selecionar_pagamento(metodo):
            alerta_pagamento.open = False
            page.update()
            processar_compra(metodo)

        alerta_pagamento = ft.AlertDialog(
            bgcolor="#0D004E",
            title=ft.Text("Método de Pagamento", weight="bold", color="white"),
            
            content=ft.Column(
                [
                    ft.Text("Escolha como deseja pagar:", size=16, color="white70"),
                    ft.Divider(color="white24"),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.QR_CODE_2, color="white"),
                        title=ft.Text("Pix (Rápido e Seguro)", color="white"),
                        subtitle=ft.Text("Aprovação instantânea", color="white70", size=12),
                        on_click=lambda _: selecionar_pagamento("Pix")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CREDIT_CARD, color="white"),
                        title=ft.Text("Cartão de Crédito", color="white"),
                        subtitle=ft.Text("Aré 12x sem juros", color="white70", size=12),
                        on_click=lambda _: selecionar_pagamento("Cartão")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.RECEIPT_LONG, color="white"),
                        title=ft.Text("Boleto Bancário", color="white"),
                        subtitle=ft.Text("Até 3 dias úteis", color="white70", size=12),
                        on_click=lambda _: selecionar_pagamento("Boleto")
                    ),
                ], 
                tight=True,
                spacing=5
            ),
            actions=[
                ft.TextButton(
                    "Cancelar", 
                    on_click=lambda _: setattr(alerta_pagamento, "open", False) or page.update(), 
                    style=ft.ButtonStyle(color="white70")
                )
            ],
        )
        page.overlay.append(alerta_pagamento)
        alerta_pagamento.open = True
        page.update()

    lista_itens = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    total = 0
    for item in cart:
        valor = float(item["valor_evento"])
        total += valor
        lista_itens.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.EVENT_AVAILABLE, color="#0D004E"),
                        ft.Column(
                            [
                                ft.Text(item["titulo"], weight="bold", size=16, color="#0D004E"),
                                ft.Text(f"R$ {valor:.2f}", color="grey", size=14),
                            ],
                            expand=True,
                            spacing=2
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE, 
                            on_click=lambda e, i=item: remover_item(i), 
                            icon_color="red",
                            tooltip="Remover"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor="white",
                padding=15,
                border_radius=10
            )
        )

    if not cart:
        lista_itens.controls.append(ft.Text("Seu carrinho está vazio.", size=18, color="grey"))

    page.add(
        ft.Container(
            content=ft.Row(
                controls = [
                    ft.Image(src="assets/icons/logo_temporaria.png", width=35, height=35),
                    ft.Column(
                        [
                            ft.Text("Magnus", size=20, weight="bold", color="white"),
                            ft.Text("Meu Carrinho", size=16, color="white"),
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
            content=ft.Column(
                [
                    lista_itens,
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.Text(f"Total: R$ {total:.2f}", size=20, weight="bold", color="#0D004E"),
                            ft.ElevatedButton(
                                "Finalizar Compra", 
                                on_click=abrir_pagamento,
                                bgcolor="#0D004E",
                                color="white",
                                disabled=len(cart) == 0
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                expand=True
            ),
            padding=20,
            expand=True
        )
    )
