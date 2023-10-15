import flet as ft
import time


# View for Welcome Back:
class Welcome:
    def __init__(self, controller):
        # Instance:
        self.controller = controller

        # Title and Alignments:
        self.controller.page.title = "Welcome"
        self.controller.page.bgcolor = ft.colors.BLUE_GREY_50

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Display Name:
        self.display_name = None

        # Container:
        self.c = ft.Container(
            alignment=ft.alignment.center,
            width=0,
            height=0,
            border_radius=10,
            animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#004643", "#001e1d"]),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#001e1d",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
        )

        # Text Animation:
        self.display_name_text = ft.Text(
            value="Welcome,",
            color="white",
            size=30,
            weight="bold",
            font_family="arvo")

        self.d = ft.Container(
            ft.Column([
                ft.Row([
                    self.display_name_text
                ],
                    alignment=ft.MainAxisAlignment.CENTER)
                ,
                ft.Row([
                    ft.Text(
                        value="Click to proceed",
                        color="white",
                        size=15,
                        font_family="arvo"
                    )],
                    alignment=ft.MainAxisAlignment.CENTER)],
                alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            animate_opacity=750,
            opacity=0)

        # Animation:
        self.stack = ft.Stack(
            [self.c, ft.Row([self.d], alignment=ft.MainAxisAlignment.CENTER)],
            width=480,
            height=270,
        )

        # BackGround and Foreground:
        self.outer_container = ft.Container(
            content=ft.Row([self.stack], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            bgcolor="#004643",
            margin=10,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#004643",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#001e1d", "#004643"]

            ), alignment=ft.alignment.center, on_click=lambda _: self.controller.page.go("/file_uploads"))

    def animate_container(self):
        self.c.width = 480
        self.c.height = 270
        self.c.update()

    def animate_text(self):
        self.d.opacity = 1
        self.d.update()

    def animate(self):
        time.sleep(1)
        self.animate_container()
        time.sleep(1)
        self.animate_text()

    def update_display(self):
        self.display_name_text.value = F"Welcome, {self.display_name}"

    def get_view(self):
        # Get Display Name:
        self.display_name = self.controller.get_display_name()

        # Update Display Name:
        self.update_display()

        return ft.View(
            "/welcome",
            controls=[self.outer_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
