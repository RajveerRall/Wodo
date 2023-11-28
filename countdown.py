import flet as ft
import asyncio

class Countdown(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.is_recording = False

    async def startTimer(self, e=None):
        self.is_recording = True
        self.seconds = 1
        asyncio.create_task(self.update_timer())
        await self.update_async()

    async def stopTimer(self, e=None):
        self.is_recording = False

    async def update_timer(self):
        while self.seconds and self.is_recording:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
            await self.update_async()
            await asyncio.sleep(1)
            self.seconds += 1

    async def toggle_icon_button(self, e):
        if self.is_recording:
            await self.stopTimer()
            e.control.icon = ft.icons.PLAY_ARROW_OUTLINED
            e.control.tooltip = "Start"
            e.control.icon_color = {"": ft.colors.GREEN}
        else:
            await self.startTimer()
            e.control.icon = ft.icons.STOP_CIRCLE_OUTLINED
            e.control.tooltip = "Stop"
            e.control.icon_color = {"": ft.colors.RED}
        await self.update_async()


    def build(self):
        
        self.countdown = ft.Text(
            value="00:00",
            style=ft.TextThemeStyle.LABEL_SMALL,

        )
        self.start_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_OUTLINED,
            on_click=self.toggle_icon_button,
            tooltip="Start",
            selected=False,
            # style=ft.ButtonStyle(color={"selected": ft.colors.GREEN, "": ft.colors.RED}),
        )
        return ft.Row(
                    [
                self.start_button,
                self.countdown,
                    ]
                )
