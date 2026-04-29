import flet as ft
import requests
from components import card_evento, get_storage, set_storage
from config import SUPABASE_URL, HEADERS
import requests

def buscar_eventos():
    # URL padrão do PostgREST do Supabase
    url = f"{SUPABASE_URL}/eventos_db?select=*"
    try:
        response = requests.get(url, headers=HEADERS)
        return response 
    except Exception as e:
        print(f"Erro ao buscar: {e}")
        return None

def home(page):
    print("Page: Home")
    # Define o estado da página atual para controle do polling
    set_storage(page, "current_page", "home")
    
    page.title = "Home - Agenda de Eventos"
    page.window_icon = "assets/icons/logo_temporaria.png"
    page.vertical_alignment=ft.CrossAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#E8E8E8"

    def sair(): # Logout
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
    #bnt = button
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
    
    # Se tiver logado, carega os outros botoes, se não, só o login
    header_actions = [btn_carrinho]
    if logado:
        header_actions.append(btn_wallet)
        header_actions.append(logout)
    else:
        header_actions.append(btn_login)

    carrossel_parado = ft.Container(
        content=ft.Image(
            src="images/flork.png",
            height=400,
            fit="cover", # Ocupa a largura toda
        ),
        width=float("inf"), # 100% width
        alignment=ft.Alignment.CENTER,
    )

    def adicionar_carrinho(evento):
        print(f"Adicionado ao carrinho: {evento['titulo']}")
        cart = get_storage(page, "cart") or []
        
        def mostrar_feedback(texto, cor):
            # Remove snackbars antigos para não acumular
            # Colocar delay depois pra ele sumir automaticamente
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
    # print("Resposta:", response.text)
    dados = response.json()
    
    # Cards já personalizados para flet
    for a in dados:
        cards.append(card_evento(a, adicionar_carrinho))

    # Grid de Eventos Responsivo
    grid_responsivo = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=c, 
                # Considera aquele sistema da tela dividida em 12 partes, pra determinar quantos eventos vai ter de acordo com o tamanho da tela
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3}) 
                for c in cards 
            ],
        spacing=10,
        run_spacing=10
    )
    
    # Sincronizar nome do usuário
    def sincronizar_usuario():
        nome = get_storage(page, "nome")
    
        if nome:
            return nome
    
        return "Usuário"
    nome_usuario = sincronizar_usuario()
    
    page.add(
        # Header
        ft.Container(
            ft.Row(
                controls = [
                    logo,
                    texto_header,
                    ft.Container(expand=True),
                    ft.Row(controls=header_actions),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            bgcolor="#0D004E",
            padding=25,
            border_radius=10,
        ),
        # Conteúdo principal
        ft.Container(
            content=ft.Column(
                [
                    carrossel_parado,
                    # Divider pra dar um espaço sem gambiarra
                    ft.Divider(height=10, color="transparent"),
                    # Saudação com nome do usuário
                    ft.Column([
                        ft.Text(f"Olá {nome_usuario},", size=24, weight="bold", color="#0D004E"),
                        ft.Text("Novas experiências o aguardam", size=16, color="grey"),
                    ], spacing=2),
                    ft.Divider(height=10, color="transparent"),
                    grid_responsivo,
                    # Footer
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
    # Polling em tempo real (5 segundos)
    async def poll_events():
        last_data = dados
        while True:
            await asyncio.sleep(5)
            # Para o polling se o usuário não estiver mais na Home
            if get_storage(page, "current_page") != "home":
                print("Polling: Usuário saiu da Home")
                break
            
            try:
                resp = buscar_eventos()
                if resp.status_code == 200:
                    new_data = resp.json()
                    # Se mudar alguma coisa, atualiza tudo
                    if new_data != last_data:
                        print("Polling: Novos eventos encontrados! Atualizando UI...")
                        last_data = new_data
                        # Limpa os eventos antigos e adiciona os novos
                        grid_responsivo.controls.clear() 
                        
                        for ev in last_data:
                            grid_responsivo.controls.append(
                                ft.Container(
                                    content=card_evento(ev, adicionar_carrinho), 
                                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3}) # Responsividade dnv
                            )
                        page.update()
            except Exception as e:
                print(f"Polling: Erro ao sincronizar: {e}")

    asyncio.create_task(poll_events())