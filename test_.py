import flet as ft


def main(page):
    def handle_click(e):
        def handle_dlg(e):
            departure_date.pick_date()

        def handle_departure_date(e):
            departure_time.pick_time()

        def handle_departure_time(e):
            close_dlg(e)
            print(departure_date.value)
            print(departure_time.value)

        def close_dlg(e):
            dlg_modal.open = False
            page.update()


        dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Create Flight"),
        content=ft.Text("Create a new Flight"),
        actions=[
                ft.TextButton("Yes", on_click=handle_dlg),
                ft.TextButton("No", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        content_padding=ft.padding.Padding(left=300, top=30, right=300, bottom=30),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
        departure_date = ft.DatePicker(on_change=handle_departure_date)
        departure_time = ft.TimePicker(on_change=handle_departure_time)
        page.overlay.append(departure_date)
        page.overlay.append(departure_time)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    button = ft.ElevatedButton("click", on_click=handle_click)
    page.add(button)

ft.app(target=main, assets_dir='assets')
