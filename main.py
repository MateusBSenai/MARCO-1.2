import os
import sys
import flet as ft

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.main import main as app_main

if __name__ == "__main__":
    ft.app(target=app_main, assets_dir="assets")