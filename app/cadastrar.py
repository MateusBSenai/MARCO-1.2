import flet as ft 
import requests
from components import botao_home_imagem, get_storage, set_storage
from config import HEADERS, SUPABASE_URL # Importação corrigida (sem o prefixo app.)

def cadastro(page):
    set_storage(page, "current_page", "cadastro")
    print("Page: Cadastro")

    def tela_login(e): # Adicionado 'e' para o evento de clique
        page.clean()
        from login import login
        login(page)
        
    def cadastrar(e): # Adicionado 'e' para o evento de clique
        nome = nome_input.value
        email = email_input.value
        senha = senha_input.value

        if not nome or not email or not senha:
            mensagem_erro.value = "Preencha todos os campos!"
            page.update()
            return

        # URL da tabela no Supabase
        URL = f"{SUPABASE_URL}/users"
        
        # Corpo do JSON no padrão das colunas que criamos no SQL
        corpo = {
            "nome": nome,
            "email": email,
            "hash_senha": senha, # No SQL usamos 'hash_senha'
            "admin": False
        }

        try:
            # POST direto para o Supabase usando os HEADERS de autenticação
            response = requests.post(URL, json=corpo, headers=HEADERS)
            
            print("Status Cadastro:", response.status_code)
            
            if response.status_code == 201:
                print("Cadastro Realizado com sucesso!")
                mensagem_erro.value = ""
                page.clean()
                from login import login
                login(page)
            elif response.status_code == 409:
                mensagem_erro.value = "Este e-mail já está cadastrado!"
            else:
                print("Erro Supabase:", response.text)
                mensagem_erro.value = "Erro ao cadastrar. Verifique os dados."
            
            page.update()

        except Exception as erro:
            print("Erro na requisição:", erro)
            mensagem_erro.value = "Erro de conexão com o servidor!"
            page.update()
    
    # UI do Cadastro (Igual à sua original, apenas corrigindo os botões)
    texto1 = ft.Text("Cadastro", size=30, weight="bold", color="white")
    texto2 = ft.Text("Crie sua conta no AccessPass", size=18, color="white")
    
    nome_input = ft.TextField(label="Nome Completo", width=300, border_color="white", color="white")
    email_input = ft.TextField(label="E-mail", width=300, border_color="white", color="white")
    senha_input = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300, border_color="white", color="white")
    
    cadastro_button = ft.ElevatedButton(
        "Cadastrar", 
        width=300, 
        on_click=cadastrar, # Função corrigida
        bgcolor="#FFD700",
        color="#0D004E"
    )

    pagina_login = ft.TextButton(
        "Já tem conta? Login", 
        width=300,
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
        on_click=tela_login # Função corrigida
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
                                texto1, texto2, nome_input, email_input, 
                                senha_input, cadastro_button, pagina_login, mensagem_erro
                            ],
                            spacing=20,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        height=530,
                        bgcolor="#0D004E",
                        padding=50,
                        border_radius=10,
                    ),
                ),
                ft.Container(content=return_home, top=20, right=20),
            ],
        )
    )