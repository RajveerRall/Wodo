import flet as ft
from flet_route import Params, Basket

class LinkButton(ft.UserControl):
    def __init__(self, text, link):
        super().__init__()
        self.text: str = text
        self.link: str = link

    async def go_to(self, e):
        await self.page.go_async(self.link)

    def build(self):
        return ft.Container(

                ft.TextButton(
                content=ft.Text(
                f"{self.text.upper()}",
                size=20,
                color="black",
                font_family="Mont-Regular",
                ),
            on_click=self.go_to,
            data=f"{self.link}",
            ), 

                )
            # ft.Text(
            #     f"{self.text.upper()}",
            #     size=20,
            #     color="#FFFFFF",
            #     font_family="Mont-Regular",
            # ),
            # height=32,
            # width=128,
            # alignment= ft.MainAxisAlignment.CENTER,
            # border_radius=16,
            # border=12,
            # on_click=self.go_to,
            # data=f"{self.link}",
            # )


class task_analyzer(ft.UserControl):
    def __init__(self):
        super().__init__()

    async def build(self, page: ft.Page, params: Params, basket: Basket):
        self.go_home_button = LinkButton("Go Home", "/")
        self.text = ft.View( 
            controls=[
           
                self.go_home_button
            ]
        )
        return self.text