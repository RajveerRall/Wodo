import flet as ft
from playsound import playsound
from plyer import notification
import time
from datetime import datetime, timedelta
import threading
import asyncio

class Reminder(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.txt_name = ft.TextField( on_submit=self.timer_with_notification ,label="set notification timer", value="{:02d}:{:02d}".format(00,00), text_align="right", width=100)
        self.button = ft.IconButton(icon=ft.icons.ADD, selected=False, on_click=self.toggle_icon_button)
        self.is_recording = False
        self.selected = False

    async def toggle_icon_button(self, e: ft.IconButton):
        if self.is_recording:
            self.stop_recording()
            e.control.icon = ft.icons.ADD
            e.control.tooltip = "Start Recording"
        else:
            await self.start_recording()
            e.control.icon = ft.icons.REMOVE
            e.control.tooltip = "Stop Recording"
        self.selected = not self.selected
        await self.update_async()

    async def start_recording(self):
        self.is_recording = True
        # asyncio.create_task(self.timer_with_notification())
        self.recording_thread = threading.Thread(target=self.timer_with_notification, daemon=True, args=())
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        # self.recording_thread.join()
        # self.timer.stopTimer
        # self.output.release()

    def timer_with_notification(self):
        input_time = datetime.strptime(self.txt_name.value, "%M:%S")
        interval_minutes = input_time.minute * 60 + input_time.second
        # interval_seconds = interval_minutes
            # Update the text field with formatted time
        mins, secs = divmod(interval_minutes, 60)
        self.txt_name.value = "{:02d}:{:02d}".format(mins, secs)
        # interval_minutes = int(self.txt_name.value)
        while self.is_recording:
            time.sleep(interval_minutes)
            notification.notify(
                    title='Timer Notification',
                    message=f'Interval reached ({interval_minutes} minutes).',
                )

    def build(self):
        return  ft.Row(
            [
                
                self.txt_name,
                self.button,                
            ]
        )



# async def main(page: ft.Page):
#     page.title = "Flet counter example"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER

#     reminder_class = reminder()

#     # def minus_click(e):
#     #     txt_number.value = str(int(txt_number.value) - 1)
#     #     page.update()

#     # def plus_click(e):
#     #     txt_number.value = str(int(txt_number.value) + 1)
#     #     page.update()

#     await page.add_async(
#         ft.Row(
#             [
#                 # ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
#                 reminder_class,
#                 # ft.IconButton(ft.icons.ADD, on_click=plus_click),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         )
#     )

# ft.app(target=main)


# import flet as ft
# from plyer import notification
# import asyncio
# from datetime import datetime, timedelta

# class Reminder(ft.UserControl):
#     def __init__(self):
#         super().__init__()
#         self.txt_name = ft.TextField(
#             on_submit=self.timer_with_notification,
#             label="Add reminder time",
#             value="{:02d}:{:02d}".format(0, 0),
#             text_align="right",
#             width=100,
#         )

#     async def notify(self, interval_minutes):
#         asyncio.sleep(interval_minutes * 60)
#         notification.notify(
#             title="Timer Notification",
#             message=f"Interval reached ({interval_minutes} minutes).",
#         )
#         await self.timer_with_notification(None)

#     async def timer_with_notification(self, e):
#         try:
#             # Parse the time and extract minutes
#             input_time = datetime.strptime(self.txt_name.value, "%H:%M")
#             interval_minutes = input_time.hour * 60 + input_time.minute

#             # Update the text field with formatted time
#             mins, secs = divmod(interval_minutes, 60)
#             self.txt_name.value = "{:02d}:{:02d}".format(mins, secs)

#             # Create a task within the main event loop
#             await self.notify(interval_minutes)

#         except ValueError:
#             print("Invalid time format. Please enter time in HH:MM format.")

#     def build(self):
#         return ft.Column([self.txt_name])

# def main(page: ft.Page):
#     page.title = "Flet reminder example"
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER

#     reminder_class = Reminder()

#     page.add(
#         ft.Row(
#             [
#                 reminder_class,
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         )
#     )

#     page.update()

# ft.app(target=main)

