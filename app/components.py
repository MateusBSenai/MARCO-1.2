import flet as ft
from datetime import datetime


def set_storage(page, key, value):
    try:
        page.client_storage.set(key, value)
    except:
        try:
            page.session[key] = value
        except:
            if not hasattr(page, "data_store"): page.data_store = {}
            page.data_store[key] = value

def get_storage(page, key):
    try:
        val = page.client_storage.get(key)
        if val is not None: return val
    except: pass
    try:
        if key in page.session: return page.session[key]
    except: pass
    return getattr(page, "data_store", {}).get(key)

def card_evento(evento, on_add_to_cart):
    if not isinstance(evento, dict):
        return ft.Text("Erro: Dados do evento inválidos")

    try:
        data_obj = datetime.strptime(evento["data_evento"], "%Y-%m-%d")
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        data_formatada = f"{dias_semana[data_obj.weekday()]}, {data_obj.day} de {meses[data_obj.month-1]}"
    except:
        data_formatada = "Data inválida"

    try:
        valor = float(evento["valor_evento"])
        valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        valor_formatado = "Gratuito"

    if evento["foto_evento"]:
        imagem = ft.Image(
            src=evento['foto_evento'],
            height=250,
            fit="cover",
            width=float("inf")
        )
    else:
        imagem = ft.Container(
            height=250,
            bgcolor="#0D004E",
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Sem imagem", color="white", weight="bold")
        )
    informacoes_evento = ft.Column(
        spacing=3,
        controls=[
            ft.Text(evento["titulo"], size=16, weight="bold", color=ft.Colors.GREY_900, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Text(data_formatada, size=11, color="grey"),
            ft.Text(f"{evento['local_evento']}", size=11, color="grey"),
            ft.Text(valor_formatado, size=14, weight="bold", color="#0D004E"),
        ]
    )
    adicionar_carrinho = ft.ElevatedButton(
        content=ft.Text("Adicionar ao Carrinho", size=12),
        icon=ft.Icons.ADD_SHOPPING_CART,
        on_click=lambda _: on_add_to_cart(evento),
        style=ft.ButtonStyle(
            bgcolor="#0D004E",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=10
        ),
        width=float("inf")
    )
    
    card = ft.Container(
        width=320,
        bgcolor="white",
        border_radius=15,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, "black")),
        content=ft.Column(
            spacing=0,
            controls=[
                imagem,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            informacoes_evento,
                            adicionar_carrinho,
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=12,
                    expand=True,
                )
            ]
        )
    )
    return card


def botao_home(page):
    def home_click():
        page.clean()
        from home import home
        home(page)
        
    return ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="white",
        on_click=home_click,
        tooltip="Voltar para o Início"
    )

def botao_home_imagem(page):
    def home_click():
        page.clean()
        from home import home
        home(page)
    return ft.Container(
        content = ft.Image(
            src="https://cdn-icons-png.flaticon.com/128/1946/1946436.png",
            width=25,
            height=25,
        ),
        on_click=home_click
    )