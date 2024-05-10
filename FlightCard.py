import time
import random
import flet as ft
from randomVariables import Randomly
from Flight import Flight
from datetime import datetime


class FlightCard:

    def __init__(self, active_flights_dll, canceled_flights_dll, flown_flights_dll, return_page, refresh_page,
                 **kwargs):
        self.refresh_page = refresh_page
        self.return_page = return_page
        self.page = return_page()
        self.active_flight_dll = active_flights_dll
        self.canceled_flights_dll = canceled_flights_dll
        self.flown_flights_dll = flown_flights_dll
        self.flight = Flight(**kwargs)
        self.__id = self.flight.flight_id
        self.__editable = False
        self.delete_card = ft.Checkbox(value=False)
        self.flight_as_card = self.create_flight_card()
        self.prev = None
        self.next = None

    def delete_flight(self, e):
        if self in self.active_flight_dll:
            self.active_flight_dll.delete(self)
            deleted_flight = self
            deleted_flight.prev = deleted_flight.next = None
            self.canceled_flights_dll.append(deleted_flight)
        elif self in self.flown_flights_dll:
            self.flown_flights_dll.delete(self)
        else:
            self.canceled_flights_dll(self)
        self.refresh_page(e=None)

    def delete_flight_card(self):
        if self in self.active_flight_dll:
            self.active_flight_dll.delete(self)
            deleted_flight = self
            deleted_flight.prev = deleted_flight.next = None
            self.canceled_flights_dll.append(deleted_flight)
        elif self in self.flown_flights_dll:
            self.flown_flights_dll.delete(self)
        else:
            self.canceled_flights_dll(self)


    def create_flight_card(self):
        if not self.__editable:
            card = ft.Dismissible(
                key=self.__id,
                animate_opacity=300,
                content=ft.Card(
                    key=self.__id,
                    animate_opacity=300,
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{self.flight.origin}/{self.flight.destination}, {self.flight.departure_time}",
                                        color='GREEN', size=14, weight=ft.FontWeight.W_400,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Row(
                                    [
                                        ft.Text(self.id, size=16, weight=ft.FontWeight.NORMAL),
                                        ft.PopupMenuButton(
                                            icon=ft.icons.MORE_HORIZ_ROUNDED,
                                            items=[
                                                ft.PopupMenuItem(text="UPDATE", on_click=self.update_card),
                                            ],
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        width=360,
                        padding=10,
                    )
                ),  # end card
                # ----------------dismissible props
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                background=ft.Container(bgcolor=ft.colors.GREEN),
                secondary_background=ft.Container(bgcolor=ft.colors.RED),
                on_dismiss=self.delete_flight,
                #on_update=self.update_card,
                dismiss_thresholds={
                    ft.DismissDirection.END_TO_START: 0.2,
                    ft.DismissDirection.START_TO_END: 0.2,
                },
            )
        elif self.__editable == None:
            card = ft.Dismissible(
                key=self.__id,
                animate_opacity=300,
                content=ft.Card(
                    key=self.__id,
                    animate_opacity=300,
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{self.flight.origin}/{self.flight.destination}, {self.flight.departure_time}",
                                        color='GREEN', size=14, weight=ft.FontWeight.W_400,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Row(
                                    [
                                        ft.Text(self.id, size=16, weight=ft.FontWeight.NORMAL),
                                        ft.PopupMenuButton(
                                            icon=ft.icons.MORE_HORIZ_ROUNDED,
                                            items=[
                                                ft.PopupMenuItem(text="UPDATE", on_click=self.update_card),
                                                ft.PopupMenuItem(
                                                    icon=ft.icons.DELETE_FOREVER,
                                                    text="Delete FlightCard",
                                                ),
                                            ],
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        width=360,
                        padding=10,
                    )
                ),  # end card
                # ----------------dismissible props
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                background=ft.Container(bgcolor=ft.colors.GREEN),
                secondary_background=ft.Container(bgcolor=ft.colors.RED),
                on_dismiss=self.delete_flight,
                # on_update=handle_update,
                # on_confirm_dismiss=handle_confirm_dismiss,
                dismiss_thresholds={
                    ft.DismissDirection.END_TO_START: 0.2,
                    ft.DismissDirection.START_TO_END: 0.2,
                },
            )
        else:
            card = ft.Card(
                key=self.__id,
                animate_opacity=300,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{self.flight.origin}/{self.flight.destination}", color='GREEN', size=14,
                                    weight=ft.FontWeight.W_400,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Row(
                                [
                                    ft.Text(self.id, size=16, weight=ft.FontWeight.NORMAL),
                                    self.delete_card
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER

                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    width=360,
                    padding=10,

                )
            )
        return card

    def isEditable(self):
        return self.__editable

    def changeEditable(self):
        self.__editable = not self.__editable
        self.flight_as_card = self.create_flight_card()

    @property
    def id(self):
        return self.__id

    def animate_card_on_search(self, e):
        if self.flight_as_card == e.control.data.flight_as_card:
            time.sleep(0.3)
            for i in range(4):
                if self.flight_as_card.content.variant == "FILLED":
                    self.flight_as_card.content.variant = "ELEVATED"
                else:
                    self.flight_as_card.content.variant = "FILLED"
                time.sleep(0.3)
                self.flight_as_card.update()

    def __lt__(self, other):
        # Define priority based on departure time; earlier flights have higher priority
        return self.flight.priority < other.flight.priority

    def __gt__(self, other):
        return self.flight.priority > other.flight.priority

    def __str__(self):
        return f'{self.flight.flight_id} : {self.flight.priority}'

    # ---------------------- EVENTS ASSOCIATED WITH EACH CARD --------------------------------
    def update_card(self, e):

        def handle_dlg(e):
            departure_date.pick_date()

        def handle_departure_date(e):
            departure_time.pick_time()

        def handle_departure_time(e):
            close_dlg(e)
            self.flight.airplane_type = airplane_type.value if airplane_type.value else self.flight.airplane_type
            self.flight.origin = Randomly.get_destination(origin.value[:3]) if origin.value else self.flight.origin
            self.flight.flight_type = flight_type.value if flight_type.value else self.flight.flight_type
            self.flight.destination = Randomly.get_destination(
                destination.value[:3]) if destination.value else self.flight.destination
            self.flight.departure_time = combine_date_and_time(departure_date.value, departure_time.value)
            self.refresh_page(e=None)
              #everything has to be written in our log file but if the flight is updated or
            #deleted it is also referenced in another log file
            self.keep_flight_log(file_status='update')
            reason = reasons_to_update.value if reasons_to_update else "Weather Conditions"
            description = text_box.value if text_box.value else "no description provided"
            self.update_flight_log(update=True, reason=reason, description=description)
            print(reasons_to_update.value)
            print(text_box.value)

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

        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        def handle_confirm_change(e):
            if e.data == "Other":
                text_box.disabled = False
            else:
                text_box.disabled = True
            self.page.update()
            # reason = reasons_to_update.value if reasons_to_update else "Weather Conditions"
            # description = text_box.value if text_box.value else "no description provided"


        text_box = ft.TextField(hint_text="Please specify", disabled=True, label="Reason to update",
                                helper_text="Required if you choose other")
        reasons_to_update = ft.Dropdown(options=[
            ft.dropdown.Option(reason) for reason in Randomly.get_cancellation_reasons()],
            label="Reason to update", helper_text="Reason to update", on_change=handle_confirm_change)

        airplane_type = ft.Dropdown(options=Randomly.get_air_planes(), label=self.flight.airplane_type,
                                    hint_content=self.flight.airplane_type, helper_text="Airplane type")
        origin = ft.Dropdown(options=Randomly.get_airport_codes(is_local=True), label=self.flight.origin,
                             hint_content=self.flight.origin, helper_text="Origin")
        destination = ft.Dropdown(options=Randomly.get_airport_codes(), label=self.flight.destination,
                                  hint_content=self.flight.destination, helper_text="Destination")
        flight_type = ft.Dropdown(options=[
            ft.dropdown.Option("Local"),
            ft.dropdown.Option("International")], label=self.flight.flight_type, hint_content=self.flight.flight_type,
            helper_text="Flight type")
        form = ft.Column([
            ft.Row([
                flight_type,
                airplane_type,
            ]),
            ft.Row([
                origin,
                destination,
            ]),
            ft.Row([
                reasons_to_update,
                text_box,
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
        departure_date = ft.DatePicker(on_change=handle_departure_date, current_date=self.flight.departure_time.date(),
                                       first_date=datetime.now())
        departure_time = ft.TimePicker(on_change=handle_departure_time, value=self.flight.departure_time.time(), )
        self.page.overlay.append(departure_date)
        self.page.overlay.append(departure_time)
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()

    # ---------------------- END EVENTS ASSOCIATED WITH EACH CARD --------------------------------
    # ----------------------- METHODS TO KEEP TRACK OF LOG FILE ----------------------------------
    def update_flight_log(self, **kwargs):
        import csv
        if self in self.flown_flights_dll:
            return
        if len(kwargs) <= 0:
           kwargs['reason'] = 'Weather Conditions'
           kwargs['description'] = 'no description provided'
        with open('assets/charts/flight_charts_upd_del.csv', mode='a', newline='') as csv_file:
            fieldnames = ['flightId', 'updatedAt', 'updatedDate', 'reason', 'description']

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            start_pos = csv_file.tell()
            if start_pos == 0:
                writer.writeheader()
            writer.writerow(
                {'flightId': str(self.flight.flight_id),
                 'updatedAt': str(datetime.now().strftime("%d/%m/%Y")),
                 'updatedDate': str(self.flight.departure_time.strftime("%d/%m/%Y")),
                 'reason': kwargs.get('reason'),
                 'description': kwargs.get('description')
                 }
            )

    def keep_flight_log(self, **kwargs):
        import csv
        if self in self.flown_flights_dll:
            return
        if len(kwargs) == 0:
            if self in self.active_flight_dll:
                file_status = "create"
            elif self in self.canceled_flights_dll:
                file_status = "delete"
        else:
            file_status = kwargs.get('file_status')

        with open('assets/charts/flight_charts.csv', mode='a', newline='') as csv_file:
                fieldnames = ['flightId', 'crud', 'createdAt', 'flightType', 'from', 'to', 'airplaneType', 'fliedAt']

                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                # Get the current position before writing the header
                start_pos = csv_file.tell()

                # Write the header only if it hasn't been written before
                if start_pos == 0:
                    writer.writeheader()
                writer.writerow(
                    {'flightId': str(self.flight.flight_id),
                     'crud': file_status,
                     'createdAt': str(self.flight.departure_time.strftime("%d/%m/%Y")),
                     'flightType': str(self.flight.flight_type),
                     'from': str(self.flight.origin),
                     'to': str(self.flight.destination),
                     'airplaneType': str(self.flight.airplane_type),
                     'fliedAt': str(self.flight.departure_time.strftime("%d/%m/%Y"))
                     }
                )


    # ----------------------- END METHODS TO KEEP TRACK OF LOG FILE ----------------------------------


class DLL:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, flight_card):

        if not self.head:
            self.head = self.tail = flight_card
        else:
            self.tail.next = flight_card
            flight_card.prev = self.tail
            self.tail = flight_card
        flight_card.keep_flight_log()

    def prepend(self, flight_card):
        flight_card.next = self.head
        if self.head:
            self.head.prev = flight_card
        else:
            self.tail = flight_card
        self.head = flight_card

    def delete(self, flight_card):
        flight_card.keep_flight_log(file_status='delete')
        flight_card.update_flight_log()
        if flight_card == self.head:
            self.head = flight_card.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif flight_card == self.tail:
            self.tail = flight_card.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            if flight_card.prev:
                flight_card.prev.next = flight_card.next
            if flight_card.next:
                flight_card.next.prev = flight_card.prev

    def delete_first(self):
        if self.head:
            deleted_flight_card = self.head
            self.head = deleted_flight_card.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
            return deleted_flight_card
        else:
            return None

    def clear(self):
        self.head = None
        self.tail = None

    def display(self):
        current = self.head
        while current:
            current = current.next

    def replace(self, old_node, new_node):
        # Traverse the doubly linked list to find the old node
        current = self.head
        while current:
            if current == old_node:
                # Found the old node, now replace it with the new node
                if current.prev:
                    current.prev.next = new_node
                else:
                    # If the old node is the head, update the head pointer
                    self.head = new_node
                if current.next:
                    current.next.prev = new_node
                else:
                    # If the old node is the tail, update the tail pointer
                    self.tail = new_node
                # Update the new node's pointers to maintain the linked list
                new_node.prev = current.prev
                new_node.next = current.next
                # Clear the old node's pointers to detach it from the linked list
                current.prev = None
                current.next = None
                return True  # Return True if replacement is successful
            current = current.next
        return False  # Return False if the old node is not found in the list

    def append_flight(self, flight_card: FlightCard):
        flight_card.prev = flight_card.next = None
        new_card = FlightCard(flight_card.active_flight_dll, flight_card.canceled_flights_dll, flight_card.flown_flights_dll, return_page=flight_card.return_page, refresh_page=flight_card.refresh_page)
        new_card.flight = flight_card.flight
        self.append(new_card)

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
