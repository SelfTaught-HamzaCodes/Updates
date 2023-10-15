import flet as ft


class TrailExpired:
    def __init__(self, controller):
        # Instance:
        self.controller = controller

        # Title and Alignments:
        self.controller.page.title = "File Uploads"
        self.controller.page.bgcolor = ft.colors.BLUE_GREY_50

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Main Heading:
        heading = ft.Text("Breaking News",
                          color="#1D976C",
                          font_family="arvo",
                          weight=ft.FontWeight.W_800,
                          style=ft.TextThemeStyle.HEADLINE_LARGE)

        # Main Body:
        body = ft.Text("We are sorry to announce that your trail has expired. \n"
                       "Thank you for using this software and for your valuable feedback. \n"
                       "We're taking a brief pause to work on enhancements and prepare to make this application open for everyone to enjoy.\n"
                       " Stay tuned for updates on our progress! Your support means a lot to us.",
                       color="#1D976C",
                       font_family="arvo",
                       text_align=ft.TextAlign.CENTER,
                       weight=ft.FontWeight.W_300,
                       style=ft.TextThemeStyle.TITLE_MEDIUM)

        # Submit Feedback:
        submit_feedback = ft.ElevatedButton(
            content=ft.Text("Login", font_family="arvo", color=ft.colors.WHITE),
            bgcolor="#1D976C",
            on_click=lambda _: self.controller.change_route("/sign_in"),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ))

        # Placement for Body:
        body_container = ft.Column([
            ft.Row([heading], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([body], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([submit_feedback], alignment=ft.MainAxisAlignment.CENTER)

        ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER)

        # Body Container
        body = ft.Container(
            content=body_container,
            border_radius=5,
            bgcolor=ft.colors.WHITE,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["white", ft.colors.BLUE_GREY_100]
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#004643",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.NORMAL
            ),
            margin=250,
            padding=20,
        )

        # Main Container:
        # background = ft.Container(
        #     ft.Image(
        #         src="Assets/Images/feedback.jpg",
        #         fit=ft.ImageFit.COVER,
        #     ))

        # Placement:
        # self.oc = ft.Row([
        #     ft.Stack(
        #         [background, ft.Column([body], alignment=ft.MainAxisAlignment.CENTER, expand=True)]
        #         , expand=True)],
        #     alignment=ft.MainAxisAlignment.CENTER)

        self.oc = ft.Container(
            content=body,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1D976C", "#93F9B9"]
            )

        )

    # Return View:
    def get_view(self):
        return ft.View(
            "/trail_expired",
            controls=[self.oc],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
