import flet as ft
import validators


class ForgetPassword:
    def __init__(self, controller):
        # Instance:
        self.controller = controller

        # Title and Alignments:
        self.controller.page.title = "Forget Password"
        self.controller.page.bgcolor = ft.colors.BLUE_GREY_50

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Email:
        self.email = None

        # OTP:
        self.otp = None

        # New Password and Confirmation:
        self.new_pw = None
        self.cfm_pw = None

        # Mini-view:
        self.view = 0

        # Main Container:
        self.oc = None

        # Main Heading:
        self.heading_c = ft.Text("Password Recovery",
                                 color="#1D976C",
                                 font_family="arvo",
                                 weight=ft.FontWeight.W_800,
                                 style=ft.TextThemeStyle.HEADLINE_LARGE)

        # View 1-A:
        self.email_c = ft.TextField(
            label="Enter your email address.",
            label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
            text_style=ft.TextStyle(font_family="arvo", color="#1D976C")
        )

        # View 1-B:
        self.otp_c = ft.TextField(
            label="Enter One-Time Password (OTP).",
            label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
            text_style=ft.TextStyle(font_family="arvo", color="#1D976C")
        )

        # View 1-C:
        self.new_pw_c = ft.TextField(
            label="Enter your new password.",
            password=True, can_reveal_password=True,
            label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
            text_style=ft.TextStyle(font_family="arvo", color="#1D976C"))

        self.cfm_pw_c = ft.TextField(
            label="Enter your password confirmation.",
            password=True, can_reveal_password=True,
            label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
            text_style=ft.TextStyle(font_family="arvo", color="#1D976C"))

        # Error Message:
        self.error = ft.Text(value="",
                             visible=False,
                             color=ft.colors.RED_900,
                             style=ft.TextThemeStyle.LABEL_LARGE,
                             weight=ft.FontWeight.W_500,
                             font_family="arvo")

        # Back Button:
        self.back_button_c = ft.ElevatedButton(
            content=ft.Text("Previous", font_family="arvo", color=ft.colors.WHITE),
            bgcolor="#1D976C",
            disabled=True,
            on_click=lambda _: self.load_view(-1),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ))

        # Forward Button:
        self.next_button_c = ft.ElevatedButton(
            content=ft.Text("Continue", font_family="arvo", color=ft.colors.WHITE),
            bgcolor="#1D976C",
            on_click=lambda _: self.load_view(1),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ))

    def load_view(self, change=0, render=False):

        # Validations:

        # Validate email address:
        if not validators.email(self.email_c.value) and change != 0:
            self.error_message("Invalid Email!")
            return False

        # Validate OTP:
        if (self.view + change) == 2 and change != 0:

            response = self.controller.model.validate_otp(self.email, self.otp_c.value)

            if response != "200":
                self.error_message(response)
                return False

        # Validate New Password and Confirmation Password:
        if (self.view + change) == 3 and change != 0:

            # Mis-match between new password:
            if self.new_pw_c.value != self.cfm_pw_c.value:
                self.error_message("Passwords don't match!")
                return False

            # In-correct password:
            if not (self.new_pw_c.value.isalnum()) or not (8 <= len(self.new_pw_c.value) <= 15):
                self.error_message("Password should only be Alpha-numeric and 8 - 15 characters long")
                return False

            # In-correct password:
            if not (self.cfm_pw_c.value.isalnum()) or not (8 <= len(self.cfm_pw_c.value) <= 15):
                self.error_message("Password should only be Alpha-numeric and 8 - 15 characters long")
                return False

        # CHANGE PASSWORD AND IF DONE SUCCESSFULLY CONTINUE TO VIEW 3, ELSE DISPLAY SERVER SIDE ERROR:
        if (self.view + change) == 3 and change != 0:

            response = self.controller.model.change_password(self.new_pw_c.value)

            if response != "200":
                self.error_message(response)
                return False

        # Hide Error:
        self.error.visible = False

        # Update current mini-view:
        self.view += change

        self.view = 0 if self.view < 0 else self.view

        # Add / Remove the Latest Controls:
        self.oc = None
        container = None

        # Back button disable logic:
        self.back_button_c.disabled = True if not self.view else False

        # View A:
        if not self.view:
            # Reset Email:
            self.email = None
            self.email_c.value = None

            container = ft.Column([
                ft.Row([self.heading_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.email_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.error], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.back_button_c, self.next_button_c], alignment=ft.MainAxisAlignment.CENTER)
            ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER)

        # View B:
        if self.view == 1:

            # Get Email:
            self.email = self.email_c.value

            # Send OTP:
            response = self.controller.model.send_otp(self.email)
            if response != "200":
                self.error_message(response)
                return False

            # Reset OTP:
            self.otp = None
            self.otp_c.value = None

            container = ft.Column([
                ft.Row([self.heading_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.otp_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.error], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.back_button_c, self.next_button_c], alignment=ft.MainAxisAlignment.CENTER)
            ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER)

        if self.view == 2:
            # Get OTP:
            self.otp = self.otp_c.value

            # Reset New Password and Confirmation Password:
            self.new_pw = None
            self.cfm_pw = None

            self.new_pw_c.value = None
            self.cfm_pw_c.value = None

            container = ft.Column([
                ft.Row([self.heading_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.new_pw_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.cfm_pw_c], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.error], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([self.back_button_c, self.next_button_c], alignment=ft.MainAxisAlignment.CENTER)
            ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER)

        if self.view == 3:
            container = ft.Column([
                ft.Row([self.heading_c],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([ft.Text("Password changed successfully!", color="#1D976C", font_family="arvo")],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(thickness=2),
                ft.Row([ft.ElevatedButton(text="Login",
                                          bgcolor="#1D976C",
                                          color="WHITE",
                                          on_click=lambda _: self.controller.change_route("/sign_in"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5)
                                          ))],
                       alignment=ft.MainAxisAlignment.CENTER)
            ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER)

        # Body Container
        body = ft.Container(
            content=container,
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
        # # Main Container:
        # background = ft.Container(
        #     ft.Image(
        #         src="Assets/Images/feedback.jpg",
        #         fit=ft.ImageFit.FILL,
        #         expand=True,
        #     ))

        # # Placement:
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

        if not render:
            self.controller.page.views.clear()
            self.controller.page.views.append(self.oc)
            self.controller.page.update()

    # Display Error Messages:
    def error_message(self, prompt):

        self.error.visible = True
        self.error.value = prompt
        self.controller.page.update()

    # Return View:
    def get_view(self):

        self.load_view(render=True)

        return ft.View(
            "/forget_password",
            controls=[self.oc],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
