import flet as ft
import requests
from components import card_evento, get_storage, set_storage
from config import SUPABASE_URL, HEADERS
import requests

def buscar_eventos():
    url = f"{SUPABASE_URL}/eventos_db?select=*"
    try:
        response = requests.get(url, headers=HEADERS)
        return response 
    except Exception as e:
        print(f"Erro ao buscar: {e}")
        return None

def home(page):
    print("Page: Home")
    set_storage(page, "current_page", "home")
    
    page.title = "Home - Agenda de Eventos"
    page.window_icon = "assets/icons/logo_temporaria.png"
    page.vertical_alignment=ft.CrossAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#E8E8E8"

    def sair():
        set_storage(page, "current_page", "logout")
        set_storage(page, "logado", False)
        set_storage(page, "email", None)
        set_storage(page, "nome", None)
        ir_login()
    
    def ir_carrinho():
        set_storage(page, "current_page", "carrinho")
        page.clean()
        from carrinho import carrinho
        carrinho(page)
    
    def ir_wallet():
        set_storage(page, "current_page", "wallet")
        page.clean()
        from wallet import wallet
        wallet(page)
    
    def ir_login():
        set_storage(page, "current_page", "login")
        page.clean()
        from login import login
        login(page)

    texto1 = ft.Text("Magnus", size=20, weight="bold")
    texto2 = ft.Text("A sua agenda de eventos.", size=16)
    texto_header = ft.Column(
        controls=[ texto1, texto2 ],
        alignment=ft.CrossAxisAlignment.START,
        spacing=0
    )
    
    logo = ft.Image(
        src="assets/icons/logo_temporaria.png",
        width=35,
        height=35
    )
    btn_carrinho = ft.IconButton(
        icon=ft.Icons.SHOPPING_CART,
        on_click=ir_carrinho,
        icon_color="white",
        tooltip="Carrinho"
    )

    btn_wallet = ft.IconButton(
        icon=ft.Icons.WALLET,
        on_click=ir_wallet,
        icon_color="white",
        tooltip="Minha Carteira"
    )

    btn_login = ft.TextButton(
        "Login", 
        on_click=ir_login,
        style=ft.ButtonStyle(color="white")
    )

    logout = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        on_click=sair,
        icon_color="white",
        tooltip="Sair"
    )
    
    logado = get_storage(page, "logado")
    
    header_actions = [btn_carrinho]
    if logado:
        header_actions.append(btn_wallet)
        header_actions.append(logout)
    else:
        header_actions.append(btn_login)

    carrossel_parado = ft.Container(
        content=ft.Image(
            src="assets/images/flork.png",
            height=400,
            fit="cover", 
        ),
        width=float("inf"), 
        alignment=ft.Alignment.CENTER,
    )

    def adicionar_carrinho(evento):
        print(f"Adicionado ao carrinho: {evento['titulo']}")
        cart = get_storage(page, "cart") or []
        
        def mostrar_feedback(texto, cor):
            page.overlay.clear() 
            snack = ft.SnackBar(
                ft.Text(texto),
                bgcolor=cor,
                action="Fechar",
                on_action=lambda _: setattr(snack, "open", False) or page.update()
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

        if not any(item['id'] == evento['id'] for item in cart):
            cart.append(evento)
            set_storage(page, "cart", cart)
            mostrar_feedback(f"{evento['titulo']} adicionado!", "green")
        else:
            mostrar_feedback("Este evento já está no carrinho!", "orange")
            print("Erro! Item no carrinho!")

    cards = []
    response = buscar_eventos()
    print("Status:", response.status_code)
    dados = response.json()
    for a in dados:
        cards.append(card_evento(a, adicionar_carrinho))

    # Grid de Eventos Responsivo
    grid_responsivo = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=c, 
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3}) 
                for c in cards 
            ],
        spacing=10,
        run_spacing=10
    )
    def sincronizar_usuario():
        nome = get_storage(page, "nome")
    
        if nome:
            return nome
    
        return "Usuário"
    nome_usuario = sincronizar_usuario()
    
    page.add(
        ft.Container(
            content=ft.Row(
                controls=[
                    logo,
                    # Envolvemos o texto em uma coluna com expand para ele ocupar o espaço 
                    # disponível e empurrar os ícones para a direita sem jogá-los fora da tela
                    ft.Column([texto1, texto2], spacing=0, expand=True), 
                    ft.Row(
                        controls=header_actions,
                        spacing=0, # Reduz o espaço entre ícones no celular
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                # Remova o expand=True daqui se ele estiver dentro de um Container fixo
            ),
            bgcolor="#0D004E",
            padding=ft.padding.only(left=15, right=10, top=10, bottom=10),
            border_radius=10,
        ),
        ft.Container(
            content=ft.Column(
                [
                    carrossel_parado,
                    ft.Divider(height=10, color="transparent"),
                    ft.Column([
                        ft.Text(f"Olá {nome_usuario},", size=24, weight="bold", color="#0D004E"),
                        ft.Text("Novas experiências o aguardam", size=16, color="grey"),
                    ], spacing=2),
                    ft.Divider(height=10, color="transparent"),
                    grid_responsivo,
                    ft.Container(
                        content=ft.Text("© 2026 Marcos. Todos os direitos reservados kkk. (E agora atualizado por Bene)", size=12, color="white"),
                        alignment=ft.Alignment.CENTER,
                        padding=10,
                        bgcolor="#0D004E",
                        border_radius=5
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
            ),
            expand=True,
            padding=10,
        )
    )

    import asyncio
    async def poll_events():
        last_data = dados
        while True:
            await asyncio.sleep(5)
            if get_storage(page, "current_page") != "home":
                print("Polling: Usuário saiu da Home")
                break
            
            try:
                resp = buscar_eventos()
                if resp.status_code == 200:
                    new_data = resp.json()
                    if new_data != last_data:
                        print("Polling: Novos eventos encontrados! Atualizando UI...")
                        last_data = new_data
                        grid_responsivo.controls.clear() 
                        
                        for ev in last_data:
                            grid_responsivo.controls.append(
                                ft.Container(
                                    content=card_evento(ev, adicionar_carrinho), 
                                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3})
                            )
                        page.update()
            except Exception as e:
                print(f"Polling: Erro ao sincronizar: {e}")

    asyncio.create_task(poll_events())