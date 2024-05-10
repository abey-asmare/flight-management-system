import time
import random

import flet as ft
from FlightCard import FlightCard, DLL

# FLIGHTS = [FlightCard() for i in range(1, 25)]
FLIGHTS = DLL()
for i in range(1, 25):
    FLIGHTS.append(FlightCard(FLIGHTS, FLIGHTS, FLIGHTS))


# todo: use minHeap instead of a heap -- tick
# todo: make the events listen and have a proper functionality
# todo: add a django register page for register interface
# todo: have 3 airplane runaways and use a proper asset
#      and also make the cards disappear and in the search suggestions
#      when the plane reaches to the end of the window

# todo: add a login page
# todo: add a update/create/read page(one page)
# todo: make the done button work
# todo: have another incoming, deleted card lists
# todo: make it work with the browser window use framework like flet-django
# todo:


def main(page):
    page.theme_mode = 'dark'

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        print(page.theme_mode)
        page.update()
        time.sleep(0.5)
        theme_toggle.selected = not theme_toggle.selected
        page.update()

    theme_toggle = ft.IconButton(
        icon="light_mode",
        on_click=change_theme,
        selected_icon="dark_mode",
        style=ft.ButtonStyle(
            color={"": ft.colors.WHITE, "selected": ft.colors.BLACK}
        )
    )

    # page.theme_mode = 'light'
    def delete_flights(e):
        add_button.disabled = True
        filter_button.disabled = True
        col.controls.clear()
        col.controls.append(nav_bar_delete)
        for flight in FLIGHTS:
            flight.changeEditable()
            col.controls.append(flight.flight_as_card)
        col.update()
        print("delete flights")

    def navigate_to_flight(e):
        text = e.control.data.id
        print(f"text: {text}")
        search_bar.close_view(text)
        selected_flight = e.control.data
        selected_card = selected_flight.flight_as_card
        print(type(selected_card))
        print(selected_card.key)
        col.scroll_to(key=selected_card.key, duration=1000)
        selected_flight.animate_card_on_search(e)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    page.title = "Card Example"
    col = ft.Column(
        spacing=6,
        width=340,
        height=page.height - 60,
        scroll=ft.ScrollMode.ALWAYS,
        col={"sm": 12, "md": 4, "xl": 4}
    )

    search_bar = ft.SearchBar(
        view_elevation=4,
        width=200,
        height=40,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Search flights",
        view_hint_text="Suggested Flights",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(flight.id), on_click=navigate_to_flight, data=flight, key=flight.id)
            for flight in FLIGHTS
        ],
    )

    def update_search_bar():
        search_bar.controls.clear()
        for flight_card in FLIGHTS:
            print(flight_card)
            search_bar.controls.append(
                ft.ListTile(title=ft.Text(flight_card.id), on_click=navigate_to_flight, data=flight_card, key=flight.id)
            )
        search_bar.update()

    def back_to_card(e):
        add_button.disabled = False
        filter_button.disabled = False
        card_col.controls.clear()
        col.controls.clear()
        col.controls.append(nav_bar)
        for flight_card in FLIGHTS:
            if flight_card.delete_card.value:
                FLIGHTS.delete(flight_card=flight_card)

        for flight_card in FLIGHTS:
            flight_card.changeEditable()
            card_col.controls.append(flight_card.flight_as_card)
        col.controls.append(card_col)
        col.update()
        update_search_bar()

    confirm_delete_button = ft.ElevatedButton("Done", height=40, on_click=back_to_card)

    airplanes = [
        ft.Image(src='assets/plane_asset.png', height=70, rotate=1.57, animate_position=random.randint(3500, 6000)) for
        i in range(3)]

    plane_stacks = [ft.Stack([
        ft.Image(
            src="ashpalt3.png",
            fit=ft.ImageFit.CONTAIN, ),
        airplanes[i],

    ]
    ) for i in range(3)]

    def animate_container(e):
        airplanes[0].left = airplanes[1].left = airplanes[2].left = 900
        page.update()
        time.sleep(5)
        update_cards()

    def update_cards():
        for i in range(3):
            FLIGHTS.delete_first()
        update_search_bar()
        col.controls.pop()
        card_col.controls.clear()
        for flight_card in FLIGHTS:
            card_col.controls.append(flight_card.flight_as_card)
        col.controls.append(card_col)
        col.update()
        row.controls.clear()
        row.controls.append(col)
        row.controls.append(right_col)
        row.update()
        page.update()


    add_button = ft.IconButton(icon=ft.icons.ADD, icon_color='#9ECAFF', on_click=animate_container)
    filter_button = ft.PopupMenuButton(
        icon=ft.icons.FILTER_LIST,
        icon_color='#9ECAFF',
        items=[
            ft.PopupMenuItem(text="Sort by id"),

            ft.PopupMenuItem(
                icon=ft.icons.DELETE_FOREVER,
                text="Delete Flights",
                on_click=delete_flights
            ),
        ],
    )
    nav_bar = ft.Row(controls=[
        search_bar,
        add_button,
        filter_button,
        theme_toggle
    ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=360
    )
    col.controls.append(
        nav_bar
    )

    nav_bar_delete = ft.Row(controls=[
        confirm_delete_button, add_button, filter_button, theme_toggle
    ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=360
    )

    # Append FlightCard objects from FLIGHTS list
    card_col = ft.Column()
    for flight in FLIGHTS:
        flight_card = flight.flight_as_card
        card_col.controls.append(flight_card)
    col.controls.append(card_col)
    # --------------------------RIGHT SIDE---------------------------------------

    # Create a Column for the right side
    right_col = ft.Column(
        col={"sm": 0, "md": 8, "xl": 8},
        expand=True,
        controls=
        plane_stacks
    )

    # --------------------------END RIGHT SIDE---------------------------------------

    row = ft.ResponsiveRow(
        [col, right_col],

    )
    page.add(row)


# Start the app
ft.app(target=main, assets_dir='assets')
