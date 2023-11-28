import flet as ft
import pyautogui
import os
from datetime import datetime
from win32api import GetSystemMetrics
import threading
import flet as ft
import cv2
import numpy as np
from os import *
import csv
import json
from flet_route import Routing, path
from flet_route import Params, Basket
from task_analyze import task_analyzer
import asyncio
from countdown import Countdown
from reminder import Reminder

# tasks = task.Task()

class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.recording_thread = None
        self.selected = None
        self.is_recording = False
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.dim = (width, height)
        self.task_folder = os.path.join(os.getcwd(), self.task_name)
        os.makedirs(self.task_folder, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.video_name = f"{self.task_name}_{self.timestamp}.mp4"
        self.fps = 30.0
        self.timer = Countdown()
        self.notification = Reminder()

    def build(self):
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                            ft.IconButton(
                            ft.icons.PLAY_ARROW_OUTLINED,
                            tooltip="Start",
                            on_click=self.toggle_icon_button,
                        ),
                        self.timer,
                        ft.VerticalDivider(width=10, thickness=5, color="grey"),
                        self.notification,
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.completed = self.display_task.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)
    
    # async def start_screenshot(self, e):
    #     task_folder = os.path.join(os.getcwd(), self.task_name)
    #     os.makedirs(task_folder, exist_ok=True)

    #     screenshot = pyautogui.screenshot()
    #     screenshot_name = f"screenshot_{time.time()}.png"
    #     screenshot_path = os.path.join(task_folder, screenshot_name)
    #     screenshot.save(screenshot_path)
    #     # await self.task_record(self)

    async def toggle_icon_button(self, e: ft.IconButton):
        if self.is_recording:
            self.stop_recording()
            e.control.icon = ft.icons.PLAY_ARROW_OUTLINED
            e.control.tooltip = "Start Recording"
            e.control.icon_color = {"": ft.colors.GREEN}
        else:
            self.start_recording()
            e.control.icon = ft.icons.STOP_CIRCLE_OUTLINED
            e.control.tooltip = "Stop Recording"
            e.control.icon_color = {"": ft.colors.RED}
            
        self.selected = not self.selected
        await self.update_async()

    def start_recording(self):
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.output.release()
        # if self.recording_thread:
        #     self.recording_thread.join()  # Wait for the recording thread to finish
        # self.output.release()
        
    def record_screen(self):

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.output = cv2.VideoWriter(os.path.join(self.task_folder, self.video_name), self.fourcc, self.fps, self.dim)

        while self.is_recording:
            # Capture the screen and write it to the video file
            screen = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
            self.output.write(frame)
            


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

class sidebar(ft.UserControl):
    async def build(self, page: ft.Page, params: Params, basket: Basket):
        self.todo = TodoApp()
        self.align = ft.MainAxisAlignment.SPACE_BETWEEN,
        self.task_page_button = LinkButton("Task Analytics", "/about")
        self.rail = ft.NavigationRail(
        height=200,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        # min_width=100,
        # min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Task Analytics"),
                
            ),
        ],
        on_change=self.task_analytics_clicked,
    )
        return ft.View ( 

        controls=[
        ft.Container(
        ft.Row(

            [
                # self.rail,
                
                ft.Column(
                    [   
                        self.todo,
                        
                        self.task_page_button,

                        
                    ]
                ),
                
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ),            
        ]

        )
    
    async def task_analytics_clicked(self, page: ft.Page,):
        await page.go("/about")

class TodoApp(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True,
        )
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.items_left = ft.Text("0 items left")

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=700,
            alignment= "left",
            controls=[
                ft.Row(
                    [ft.Text(value="Todos", style="headlineMedium")], alignment="center"
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.CREATE, text="Add", on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                        ft.Divider(height=3,thickness=3, color="grey"),
                    ],
                ),
            ],   
        )
    

    async def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            await self.new_task.focus_async()
            await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                await self.task_delete(task)

    async def update_async(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        await super().update_async()


async def main(page: ft.Page):

    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    # await page.update_async()

    # # create application instance
    # app = sidebar()
    # await page.add_async(app)

    app_routes = [
        path(
            url="/",
            clear=True,  # If you want to clear all the routes you have passed so far, then pass True otherwise False.
            view=sidebar().build,  # Here you have to pass a function or method which will take page,params and basket and return ft.View (If you are using function based view then you just have to give the name of the function.)
        ),
        path(url="/about", clear=True, view=task_analyzer().build),
    ]

    Routing(
        page=page,  # Here you have to pass the page. Which will be found as a parameter in all your views
        async_is=True,
        app_routes=app_routes,  # Here a list has to be passed in which we have defined app routing like app_routes
    )

    if not page.route:
        page.route = "/"

    await page.go_async(page.route)


ft.app(target=main)