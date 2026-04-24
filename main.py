import os
import sys
import flet as ft

# Adiciona a pasta app ao path para os imports internos funcionarem
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.main import main as app_main

if __name__ == "__main__":
    # assets_dir aponta para a pasta assets na raiz
    ft.app(target=app_main, assets_dir="assets")