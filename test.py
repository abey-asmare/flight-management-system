import time
import random
import itertools
from datetime import datetime

import flet as ft
from FlightCard import FlightCard, DLL
from randomVariables import Randomly

ACTIVE_FLIGHTS_DLL = DLL()
CANCELED_FLIGHTS_DLL = DLL()
FLOWN_FLIGHTS_DLL = DLL()

def main(page):
    def update_all_cards():
        active_flight_cards.controls.clear()
        flown_flight_cards.controls.clear()
        canceled_flight_cards.controls.clear()
        for flight_card in ACTIVE_FLIGHTS_DLL:
            active_flight_cards.controls.append(flight_card.flight_as_card)
        for flight_card in FLOWN_FLIGHTS_DLL:
            flown_flight_cards.controls.append(flight_card.flight_as_card)
        for flight_card in CANCELED_FLIGHTS_DLL:
            canceled_flight_cards.controls.append(flight_card.flight_as_card)
        all_cards_wrapper_row.controls.clear()
        all_cards_wrapper_row.controls.append(active_flight_cards)
        all_cards_wrapper_row.controls.append(flown_flight_cards)
        all_cards_wrapper_row.controls.append(canceled_flight_cards)
        all_cards_wrapper_row.update()
        update_search_bar()
        page.update()

    def return_page():
        return page

    for i in range(1, 25):
        ACTIVE_FLIGHTS_DLL.append(FlightCard(ACTIVE_FLIGHTS_DLL, CANCELED_FLIGHTS_DLL, FLOWN_FLIGHTS_DLL, return_page=return_page))
    for i in range(1, 25):
        CANCELED_FLIGHTS_DLL.append(FlightCard(ACTIVE_FLIGHTS_DLL, CANCELED_FLIGHTS_DLL, FLOWN_FLIGHTS_DLL, return_page=return_page))

    for i in range(1, 25):
        FLOWN_FLIGHTS_DLL.append(FlightCard(ACTIVE_FLIGHTS_DLL, CANCELED_FLIGHTS_DLL, FLOWN_FLIGHTS_DLL, return_page=return_page))

    page.theme_mode = 'dark'
    def handle_date_change(e):
        # print(f"date value = {departure_date.value}")
        # print(f"date data = {e.data}")
        departure_time.pick_time()

    def handle_time_change(e):
        # print(f"time value = {departure_time.value}")
        # print(f"e.data = {e.data}")
        create_new_flight(e)
        close_dlg(e)

# Combine the selected date and time into a Python datetime object
    def combine_date_and_time(date, time):
        if date is not None and time is not None:
            combined_datetime = datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=time.hour,
                minute=time.minute
            )
            print("Combined datetime:", combined_datetime)
            return combined_datetime
        else:
            return None


    departure_date = ft.DatePicker(on_change=handle_date_change)
    departure_time = ft.TimePicker(on_change=handle_time_change)
    def add_elements_to_page():
        page.overlay.append(departure_date)
        page.overlay.append(departure_time)
    page.overlay.append(departure_date)
    page.overlay.append(departure_time)

    def handle_dlg(e):
        departure_date.pick_date()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def create_new_flight(e):
        dlg_modal.open = False
        destination_dictionary = Randomly.get_destination(destination.value[:3])
        new_flight = FlightCard(ACTIVE_FLIGHTS_DLL, CANCELED_FLIGHTS_DLL, FLOWN_FLIGHTS_DLL,return_page=return_page,
                                flight_type = flight_type.value,destination = destination_dictionary,
                                airplane_type = airplane_type.value,departure_time = combine_date_and_time(departure_date.value, departure_time.value),
                                origin = Randomly.get_destination(origin.value[:3]))

        ACTIVE_FLIGHTS_DLL.append(new_flight)
        active_flight_cards.controls.append(new_flight.flight_as_card)
        print(ACTIVE_FLIGHTS_DLL.tail.flight.destination)
        update_search_bar()
        update_all_cards()
        page.update()


    airplane_type = ft.Dropdown(options=Randomly.get_air_planes(), label="Airplane type")
    origin = ft.Dropdown(options=Randomly.get_airport_codes(is_local=True), label="origin")
    destination = ft.Dropdown(options=Randomly.get_airport_codes(), label="destination")
    flight_type = ft.Dropdown(options=[
        ft.dropdown.Option("Local"),
        ft.dropdown.Option("International")], label="Flight Type")

    form = ft.Column([
        ft.Row([
            flight_type,
            airplane_type,
        ]),
        ft.Row([
            origin,
            destination,
        ]),
    ])
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Create Flight"),
        content=ft.Text("Create a new Flight"),
        actions=[
            form,
            ft.Row([
                ft.TextButton("Yes", on_click=handle_dlg),
                ft.TextButton("No", on_click=close_dlg),
            ])
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        content_padding=ft.padding.Padding(left=300, top=30, right=300, bottom=30),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()


    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        print(page.theme_mode)
        page.update()
        time.sleep(0.5)
        theme_toggle.selected = not theme_toggle.selected
        page.update()

    # ------------------------  EVENT TRIGGER FUNCTIONS  ------------------------------------------------

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    def navigate_to_flight(e):
        update_search_bar()
        text = e.control.data.id
        search_bar.close_view(text)
        selected_flight = e.control.data
        selected_card = selected_flight.flight_as_card
        active_flight_cards.scroll_to(key=selected_card.key, duration=1000)
        selected_flight.animate_card_on_search(e)

    # ------------------------  END EVENT TRIGGER FUNCTIONS  ------------------------------------------------
    # ------------------------  START HELPER FUNCTIONS  ------------------------------------------------
    def update_search_bar():
        search_bar.controls.clear()
        for flight_card in ACTIVE_FLIGHTS_DLL:
            search_bar.controls.append(
                ft.ListTile(title=ft.Text(flight_card.id), on_click=navigate_to_flight, data=flight_card, key=flight.id)
            )
        for flight_card in FLOWN_FLIGHTS_DLL:
            search_bar.controls.append(
                ft.ListTile(title=ft.Text(flight_card.id), on_click=navigate_to_flight, data=flight_card, key=flight.id)
            )
        for flight_card in CANCELED_FLIGHTS_DLL:
            search_bar.controls.append(
                ft.ListTile(title=ft.Text(flight_card.id), on_click=navigate_to_flight, data=flight_card, key=flight.id)
            )
        search_bar.update()

    def delete_flights(e):
        add_button.disabled = True
        filter_button.disabled = True
        wrapper.controls.clear()
        wrapper.controls.append(nav_bar_delete)
        active_flight_cards.controls.clear()
        flown_flight_cards.controls.clear()
        canceled_flight_cards.controls.clear()

        active_flight_cards.controls.append(
            ft.Text("Active Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight in ACTIVE_FLIGHTS_DLL:
            flight.changeEditable()
            active_flight_cards.controls.append(flight.flight_as_card)
        active_flight_cards.update()

        flown_flight_cards.controls.append(
            ft.Text("Successful Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight in FLOWN_FLIGHTS_DLL:
            flight.changeEditable()
            flown_flight_cards.controls.append(flight.flight_as_card)
        flown_flight_cards.update()

        canceled_flight_cards.controls.append(
            ft.Text("Cancelled Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight in CANCELED_FLIGHTS_DLL:
            flight.changeEditable()
            canceled_flight_cards.controls.append(flight.flight_as_card)
        canceled_flight_cards.update()
        wrapper.controls.append(all_cards_wrapper_row)
        wrapper.update()

    def back_to_card(e):
        add_button.disabled = False
        filter_button.disabled = False
        wrapper.controls.clear()
        wrapper.controls.append(nav_bar)
        active_flight_cards.controls.clear()
        flown_flight_cards.controls.clear()
        canceled_flight_cards.controls.clear()

        active_flight_cards.controls.append(
            ft.Text("Active Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight_card in ACTIVE_FLIGHTS_DLL:
            if flight_card.delete_card.value:
                # tempcard = flight_card
                ACTIVE_FLIGHTS_DLL.delete(flight_card=flight_card)
                # CANCELED_FLIGHTS_DLL.append(tempcard)
            # make the append to the canceled flight work
            else:
                flight_card.changeEditable()
                active_flight_cards.controls.append(flight_card.flight_as_card)

        canceled_flight_cards.controls.append(
            ft.Text("Cancelled Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight_card in CANCELED_FLIGHTS_DLL:
            if flight_card.delete_card.value:
                CANCELED_FLIGHTS_DLL.delete(flight_card=flight_card)
            else:
                flight_card.changeEditable()
                canceled_flight_cards.controls.append(flight_card.flight_as_card)

        flown_flight_cards.controls.append(
            ft.Text("Successful Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
        for flight_card in FLOWN_FLIGHTS_DLL:
            if flight_card.delete_card.value:
                FLOWN_FLIGHTS_DLL.delete(flight_card=flight_card)
            else:
                flight_card.changeEditable()
                flown_flight_cards.controls.append(flight_card.flight_as_card)
        active_flight_cards.update()
        flown_flight_cards.update()
        canceled_flight_cards.update()
        wrapper.controls.append(all_cards_wrapper_row)
        wrapper.update()
        update_search_bar()

    # ------------------------  END HELPER FUNCTIONS  ------------------------------------------------

    theme_toggle = ft.IconButton(
        icon="light_mode",
        on_click=change_theme,
        selected_icon="dark_mode",
        style=ft.ButtonStyle(
            color={"": ft.colors.WHITE, "selected": ft.colors.BLACK}
        )
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
    )

    add_button = ft.IconButton(icon=ft.icons.ADD, icon_color='#9ECAFF', on_click=open_dlg_modal)
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
        theme_toggle,
        search_bar,
        add_button,
        filter_button
    ],
        alignment=ft.MainAxisAlignment.CENTER,

    )

    confirm_delete_button = ft.ElevatedButton("Done", height=40, on_click=back_to_card)
    nav_bar_delete = ft.Row(controls=[
        confirm_delete_button, add_button, filter_button, theme_toggle
    ],
        alignment=ft.MainAxisAlignment.CENTER,
        width=360
    )

    active_flight_cards = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        height=page.height - 120,
        spacing=6,
        width=300,
        col={"sm": 12, "md": 3, "xl": 4}
    )
    canceled_flight_cards = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        height=page.height - 120,
        spacing=6,
        width=300,
        col={"sm": 12, "md": 3, "xl": 4}
    )
    flown_flight_cards = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        height=page.height - 120,
        spacing=6,
        width=340,
        col={"sm": 12, "md": 3, "xl": 4}
    )
    active_flight_cards.controls.append(
        ft.Text("Active Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
    for flight in ACTIVE_FLIGHTS_DLL:
        flight_card = flight.flight_as_card
        active_flight_cards.controls.append(flight_card)

    flown_flight_cards.controls.append(
        ft.Text("Successful Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
    for flight in FLOWN_FLIGHTS_DLL:
        flight_card = flight.flight_as_card
        flown_flight_cards.controls.append(flight_card)
    canceled_flight_cards.controls.append(
        ft.Text("Canceled Flights", weight=ft.FontWeight.W_400, size=18, text_align=ft.TextAlign.CENTER))
    for flight in CANCELED_FLIGHTS_DLL:
        flight_card = flight.flight_as_card
        canceled_flight_cards.controls.append(flight_card)

    all_cards_wrapper_row = ft.ResponsiveRow(
        [
            active_flight_cards,
            flown_flight_cards,
            canceled_flight_cards,
        ],
    )
    wrapper = ft.Column()

    def home_page():
        wrapper.controls.append(nav_bar)
        wrapper.controls.append(all_cards_wrapper_row)
        page.add(wrapper)
        update_search_bar()



    home_page()


# Start the app
ft.app(target=main, assets_dir='assets')
