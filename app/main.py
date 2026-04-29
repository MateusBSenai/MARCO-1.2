import flet as ft
from login import login

def main(page: ft.Page):
    page.window.icon = "logo_temporaria.ico"
    login(page)