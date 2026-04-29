import flet as ft
import requests
from config import HEADERS, SUPABASE_URL
from components import botao_home_imagem, get_storage, set_storage

def login(page):
    print("Page: Login")
    set_storage(page, "current_page", "login")
    
    if get_storage(page, "logado"):
        print("Usuário já logado, redirecionando...")
        from home import home
        home(page)
        return
    
    page.title = "Login - Agenda de Eventos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#E8E8E8"

    def verificar_senha(e):
        email = email_input.value
        senha = senha_input.value

        if not email or not senha:
            mensagem_erro.value = "Preencha todos os campos!"
            page.update()
            return

        url_query = f"{SUPABASE_URL}/users?email=eq.{email}&hash_senha=eq.{senha}&select=*"

        try:
            response = requests.get(url_query, headers=HEADERS)
            
            if response.status_code == 200:
                dados = response.json()
                if len(dados) > 0:
                    user = dados[0]
                    print("Login Realizado com sucesso!")
                    
                    set_storage(page, "logado", True)
                    set_storage(page, "user_id", user["id"])
                    set_storage(page, "user_name", user["nome"])
                    set_storage(page, "is_admin", user.get("admin", False))

                    mensagem_erro.value = ""
                    page.clean()
                    if user.get("admin") == True:
                        print("Redirecionando para área ADM")
                        from admin_panel import admin_panel
                        admin_panel(page)
                    else:
                        print("Redirecionando para Home de Usuário")
                        from home import home
                        home(page)
                else:
                    mensagem_erro.value = "Email ou senha incorretos!"
            else:
                mensagem_erro.value = f"Erro no servidor: {response.status_code}"
            
            page.update()

        except Exception as erro:
            print("Erro na requisição:", erro)
            mensagem_erro.value = "Erro de conexão com o banco!"
            page.update()

    # UI do formulário
    texto1 = ft.Text("Login", size=30, weight="bold", color="white")
    texto2 = ft.Text("Bem-vindo de volta!", size=18, color="white")
    
    email_input = ft.TextField(
        label="E-mail", 
        width=300, 
        border_color="white", 
        color="white",
        focused_border_color="#FFD700"
    )
    senha_input = ft.TextField(
        label="Senha", 
        password=True, 
        can_reveal_password=True, 
        width=300, 
        border_color="white", 
        color="white",
        focused_border_color="#FFD700"
    )
    
    login_button = ft.ElevatedButton(
        "Entrar", 
        width=300, 
        on_click=verificar_senha,
        bgcolor="#FFD700",
        color="#0D004E"
    )

    def ir_cadastrar(e):
        page.clean()
        from cadastrar import cadastro
        cadastro(page)

    pagina_cadastrar = ft.TextButton(
        "Não tem conta? Cadastre-se", 
        width=300,
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
        on_click=ir_cadastrar
    )
    
    mensagem_erro = ft.Text("", color=ft.Colors.RED, weight="bold", size=14)
    return_home = botao_home_imagem(page)
    
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Container(
                        ft.Column(
                            [
                                texto1, texto2, email_input, senha_input, 
                                login_button, pagina_cadastrar, mensagem_erro
                            ],
                            spacing=20,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        bgcolor="#0D004E",
                        padding=50,
                        height=480,
                        border_radius=10,
                    ),
                    expand=True
                ),
                ft.Container(content=return_home, top=20, right=20),
            ],
        )
    )