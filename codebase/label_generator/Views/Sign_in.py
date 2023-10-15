import flet as ft
import validators


class SignIn:

    def __init__(self, controller):
        # Instance:
        self.controller = controller

        # Title and Alignments:
        self.controller.page.title = "Sign In"
        self.controller.page.bgcolor = ft.colors.BLUE_GREY_50

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Heading:
        heading = ft.Text(value="Welcome back",
                          color="#2c5282",
                          style=ft.TextThemeStyle.HEADLINE_LARGE,
                          weight=ft.FontWeight.W_500,
                          font_family="arvo")
        # Sub-Heading:
        sub_heading = ft.Text(value="Welcome back! Please enter your details.",
                              style=ft.TextThemeStyle.TITLE_SMALL,
                              weight=ft.FontWeight.W_500,
                              color=ft.colors.GREY_500,
                              font_family="arvo")

        # Error Message - Text:
        self.txt_em = ft.Text(value="",
                              visible=False,
                              color=ft.colors.RED_900,
                              style=ft.TextThemeStyle.LABEL_LARGE,
                              weight=ft.FontWeight.W_500,
                              font_family="arvo")

        # Email - Label:
        label_em = ft.Text(value="Email",
                           color="#2c5282",
                           style=ft.TextThemeStyle.TITLE_SMALL,
                           weight=ft.FontWeight.W_500,
                           font_family="arvo")

        # Email - Text Field:
        self.txt_fld_em = ft.TextField(hint_text="Enter your email",
                                       text_style=ft.TextStyle(font_family="arvo"))

        # Password - Label:
        label_pw = ft.Text(value="Password",
                           style=ft.TextThemeStyle.TITLE_SMALL,
                           color="#2c5282",
                           font_family="arvo",
                           weight=ft.FontWeight.W_500)

        # Password - Text Field:
        self.txt_fld_pw = ft.TextField(hint_text="Enter your password",
                                       password=True,
                                       text_style=ft.TextStyle(font_family="arvo"),
                                       can_reveal_password=True)

        # Remember me:
        self.remember_me_cb = ft.Checkbox(fill_color="#2c5282", value=False)

        remember_me = ft.Row([self.remember_me_cb,
                              ft.Text(value="Remember for 30 days", font_family="arvo", color=ft.colors.GREY_500,
                                      style=ft.TextThemeStyle.TITLE_SMALL)], alignment=ft.MainAxisAlignment.START)

        # Forget Password:
        # SET VIEW
        f_pw = ft.Text(spans=[ft.TextSpan("Forget Password ?",
                                          on_click=lambda _:self.controller.change_route("/forget_password"))],
                       font_family="arvo",
                       color="#2c5282")

        # Sign Up - Button:
        sign_up_btn = ft.ElevatedButton(content=ft.Text("Sign In", font_family="arvo"),
                                        width=1000,
                                        color=ft.colors.WHITE,
                                        bgcolor="#2c5282",
                                        on_click=lambda _: self.validate(),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=5)
                                        ))

        # Sign In - Label:
        sign_in_lb = ft.Text(value="Don't have an account?",
                             style=ft.TextThemeStyle.TITLE_SMALL,
                             weight=ft.FontWeight.W_500,
                             font_family="arvo")

        # Sign In - View:
        sign_in_vw = ft.Text(spans=[ft.TextSpan("Sign up for free",
                                                on_click=lambda _: self.controller.change_route("/sign_up"))],
                             font_family="arvo",
                             color="#2c5282")

        # Description
        description = ft.Container(ft.Column(
            [ft.Image(
                src=self.controller.model.resource_path("Sign_In.jpg"),
                fit=ft.ImageFit.COVER,
                expand=True,
            )]
        ), expand=True)

        # Add Controls:
        heading_column = ft.Container(ft.Column([heading, sub_heading,
                                                 self.txt_em,
                                                 label_em, self.txt_fld_em,
                                                 label_pw, self.txt_fld_pw,
                                                 ft.Row([remember_me, f_pw],
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                                 sign_up_btn,
                                                 ft.Row([sign_in_lb, sign_in_vw],
                                                        alignment=ft.MainAxisAlignment.CENTER)],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                      expand=True,
                                      padding=170,
                                      bgcolor=ft.colors.BLUE_GREY_50)

        # Main Row:
        row = ft.Row([heading_column, description], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Main Container:
        self.main_container = ft.Container(
            row,
            expand=True,
            border_radius=15,
            margin=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#2c5282",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            ))

    # Client Side Validation:
    def validate(self):
        # Validate:
        cs_valid_em, cs_valid_pw = False, False

        # Check Email:
        email = self.txt_fld_em.value

        if not validators.email(email):
            self.txt_fld_em.error_text = "Enter a valid email address."
        else:
            cs_valid_em, self.txt_fld_em.error_text = True, ""

        # Check Password:
        password = self.txt_fld_pw.value

        if not (password.isalnum()) or not (8 <= len(password) <= 15):
            self.txt_fld_pw.error_text = "Password should only be Alpha-numeric and 8 - 15 characters long"
        else:
            cs_valid_pw, self.txt_fld_pw.error_text = True, ""

        # Do Server Side Validation:
        if cs_valid_em and cs_valid_pw:

            remember = self.remember_me_cb.value

            response = self.controller.sign_in_validation(email, password, remember)

            # If signin was successful:
            if response == "200":

                # Check if newly log in user has given the feedback:
                view = self.controller.model.validate_session(self.controller.launch)

                if view == "Welcome":
                    self.controller.change_route("/file_uploads")

                elif view == "Feedback":
                    self.controller.change_route("/feedback")

                elif view == "Trail_Expired":
                    self.controller.change_route("/trail_expired")

            # Raise Error:
            else:
                self.txt_em.value = response
                self.txt_em.visible = True

        # Update page:
        self.controller.page.update()

    # Return View:
    def get_view(self):
        return ft.View(
            "/sign_in",
            controls=[self.main_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# if __name__ == "__main__":
#     ft.app(target=view)
