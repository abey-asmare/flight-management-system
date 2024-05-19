import os
import sys
import subprocess

from dotenv import load_dotenv
import flet as ft
from flet.auth.providers import GitHubOAuthProvider
import requests

load_dotenv()
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

def main(page: ft.Page):
    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",
    )

    def login_click(e):
        page.login(provider)

    def on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

        # Run the script using subprocess
        subprocess.run([sys.executable, 'test_.py'])

    page.on_login = on_login
    page.add(ft.ElevatedButton("Login with GitHub", on_click=login_click))

ft.app(target=main, port=8550, view=ft.WEB_BROWSER)
