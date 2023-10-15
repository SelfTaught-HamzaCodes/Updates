# Main entry point for our application:

# Imports:
import flet as ft
from label_generator.controller import Controller
import os
import sys


def main(page: ft.page):
    # Create an instance of the Controller class:
    Controller(page)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# if __name__ == "__main__":
ft.app(target=main)
