import flet as ft


class EmailVerification:
    def __init__(self, controller):

        # Set Instance:
        self.controller = controller

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Controls:
        verify = ft.Column([

            ft.Row([ft.Icon(name=ft.icons.EMAIL,
                            color="#1D976C",
                            size=50)],
                   alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([ft.Text(value="Verify your email address.",
                            weight=ft.FontWeight.W_800,
                            font_family="arvo",
                            style=ft.TextThemeStyle.BODY_LARGE,
                            color="#1D976C")],
                   alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([ft.Text(value="Please click on the link in the email we sent, then sign in.",
                            style=ft.TextThemeStyle.BODY_MEDIUM,
                            font_family="arvo",
                            color="#1D976C")],
                   alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([ft.ElevatedButton(content=ft.Text("Sign In", font_family="arvo"),
                                      on_click=lambda _: self.controller.change_route("/sign_in"),
                                      color=ft.colors.BLUE_GREY_50,
                                      style=ft.ButtonStyle(
                                          shape=ft.RoundedRectangleBorder(radius=5)
                                      ),
                                      bgcolor="#1D976C")],
                   alignment=ft.MainAxisAlignment.CENTER)
        ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Inner Container:
        inner_container = ft.Container(
            verify,
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_GREY_50,
            width=480,
            height=270,
            border_radius=5,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#1D976C",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
        )

        # Outer Container:
        self.outer_container = ft.Container(
            ft.Row([inner_container], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            bgcolor="#004643",
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1D976C", "#93F9B9"]
            ),

        )

    def get_view(self):

        return ft.View(
            "/verification",
            controls=[self.outer_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

