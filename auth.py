import os
import sys

from dotenv import load_dotenv
import flet as ft
from flet.auth.providers import GitHubOAuthProvider, GoogleOAuthProvider
import requests
import subprocess
from user import User

load_dotenv()
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def login_page(page: ft.Page):
    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",
    )
    google_provider = GoogleOAuthProvider(
        client_id= GOOGLE_CLIENT_ID,
        client_secret= GOOGLE_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",

    )
    page.bgcolor = '#0A0A0A'

    def login_click(e):
        page.login(provider)

    def google_login_click(e):
        page.login(google_provider)

    def google_on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {page.auth.token.access_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            # Get the user's profile image URL
            profile_image_url = user_data.get("picture")
            print()
            print("Profile Image URL:", profile_image_url)
            user = User(
                id=page.auth.user.id,
                        name=page.auth.user["name"],
                        email=page.auth.user["email"],
                        login=None,
                        profile_image_url=profile_image_url, # Google doesn't have a 'login' field, using email as a login
            )
            user.save()
            # Run the script using subprocess
            subprocess.run([sys.executable, 'main.py'])

    def on_login(e):
        print("Login error:", e.error)
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)
        print("Name:", page.auth.user["name"])
        # print("Login:", page.auth.user["login"])
        print("Email:", page.auth.user["email"])
        if isinstance(page.auth.provider, GitHubOAuthProvider):
            user_info_url = "https://api.github.com/user"
            headers = {"Authorization": f"Bearer {page.auth.token.access_token}"}
            response = requests.get(user_info_url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                # Get the user's profile image URL
                profile_image_url = user_data.get("avatar_url")
                print("Profile Image URL:", profile_image_url)
                user = User(id=page.auth.user.id,
                            name=page.auth.user["name"],
                            email=page.auth.user["email"],
                            login=page.auth.user["login"],
                            profile_image_url=profile_image_url,
                )
                user.save()
                # Run the script using subprocess
                subprocess.run([sys.executable, 'main.py'])
        elif isinstance(page.auth.provider, GoogleOAuthProvider):
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {page.auth.token.access_token}"}
            response = requests.get(user_info_url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                # Get the user's profile image URL
                profile_image_url = user_data.get("picture")
                print()
                print("Profile Image URL:", profile_image_url)
                user = User(
                    id=page.auth.user.id,
                            name=page.auth.user["name"],
                            email=page.auth.user["email"],
                            login=page.auth.user["email"],
                            profile_image_url=profile_image_url, # Google doesn't have a 'login' field, using email as a login
                )
                user.save()
                # Run the script using subprocess
                subprocess.run([sys.executable, 'main.py'])

    page.on_login = on_login
    btn_github_btn = ft.Container(
        content=ft.Row(
            [
                ft.Image('github-mark-white.png', height=20, fit=ft.ImageFit.CONTAIN),
                ft.Text("Login with Github", size=18)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border_radius=10,
        bgcolor='#24292E',
        width=300,
        height=54,
        margin=ft.margin.symmetric(horizontal=100),
        ink=True,
        on_click= login_click,
        alignment=ft.alignment.center,

    )

    btn_google_btn = ft.Container(
        content=ft.Row(
            [
                ft.Image('google-48.png', height=20, fit=ft.ImageFit.CONTAIN),
                ft.Text("Login with Google", size=18, color="#5B5B5B")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border_radius=10,
        bgcolor='#FFFFFF',
        width=300,
        height=54,
        margin=ft.margin.symmetric(horizontal=100),
        ink=True,
        on_click= google_login_click,
        alignment=ft.alignment.center,
    )

    page_content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Log into Flight Management System", size=28, font_family='sarabun', weight=ft.FontWeight.W_600,
                        color='white', text_align=ft.TextAlign.CENTER),
                btn_github_btn,
                btn_google_btn
            ],
            spacing=30,
        ),  # column
        margin=ft.margin.symmetric(vertical=140, horizontal=300),
        alignment=ft.alignment.center,
    )
    page.add(
        page_content
    )
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER


ft.app(target=login_page, port=8550, view=ft.WEB_BROWSER, assets_dir='assets')
