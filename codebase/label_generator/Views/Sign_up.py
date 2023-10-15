import flet as ft
import validators


class SignUp:
    def __init__(self, controller):
        # Set Controller:
        self.controller = controller

        # Set Title and Alignments:
        self.controller.page.title = "Sign Up"
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
        heading = ft.Text(value="Welcome",
                          color="#276749",
                          style=ft.TextThemeStyle.HEADLINE_LARGE,
                          weight=ft.FontWeight.W_500,
                          font_family="arvo")
        # Sub-Heading:
        sub_heading = ft.Text(value="Sign up for a 30-day trail, Please enter your details.",
                              style=ft.TextThemeStyle.TITLE_SMALL,
                              weight=ft.FontWeight.W_500,
                              color=ft.colors.GREY_500,
                              font_family="arvo")

        # Display Name - Label:
        label_dn = ft.Text(value="Display Name",
                           color="#276749",
                           style=ft.TextThemeStyle.TITLE_SMALL,
                           weight=ft.FontWeight.W_500,
                           font_family="arvo")

        # Error Message - Text:
        self.txt_em = ft.Text(value="",
                              visible=False,
                              color=ft.colors.RED_900,
                              style=ft.TextThemeStyle.LABEL_LARGE,
                              weight=ft.FontWeight.W_500,
                              font_family="arvo")

        # Display Name - Text Field:
        self.txt_fld_dn = ft.TextField(hint_text="Enter your display name",
                                       text_style=ft.TextStyle(font_family="arvo"))

        # Email - Label:
        label_em = ft.Text(value="Email",
                           color="#276749",
                           font_family="arvo",
                           style=ft.TextThemeStyle.TITLE_SMALL,
                           weight=ft.FontWeight.W_500)

        # Email - Text Field:
        self.txt_fld_em = ft.TextField(hint_text="Enter your email",
                                       text_style=ft.TextStyle(font_family="arvo"))

        # Password - Label:
        label_pw = ft.Text(value="Password",
                           color="#276749",
                           font_family="arvo",
                           style=ft.TextThemeStyle.TITLE_SMALL,
                           weight=ft.FontWeight.W_500)

        # Password - Text Field:
        self.txt_fld_pw = ft.TextField(hint_text="Enter your password",
                                       password=True,
                                       text_style=ft.TextStyle(font_family="arvo"),
                                       can_reveal_password=True)

        # Sign Up - Button:
        sign_up_btn = ft.ElevatedButton(content=ft.Text("Sign Up", font_family="arvo"),
                                        width=1000,
                                        bgcolor="#276749",
                                        color=ft.colors.WHITE,
                                        on_click=lambda _: self.validate(),
                                        # on_click=lambda _: self.controller.change_route("/verification"),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=5)
                                        ))

        # Sign In - Label:
        sign_in_lb = ft.Text(value="Have an account?",
                             font_family="arvo",
                             style=ft.TextThemeStyle.TITLE_SMALL,
                             weight=ft.FontWeight.W_500)

        # Sign In - View:
        sign_in_vw = ft.Text(spans=[ft.TextSpan("Sign In",
                                                on_click=lambda _: self.controller.change_route("/sign_in"))],
                             font_family="arvo",
                             color="#276749")

        # Description
        description = ft.Container(ft.Column(
            [ft.Image(
                src=self.controller.model.resource_path("Sign_Up.jpg"),
                fit=ft.ImageFit.COVER,
                expand=True,
            )]
        ), expand=True)

        # Add Controls:
        heading_column = ft.Container(ft.Column([heading, sub_heading,
                                                 self.txt_em,
                                                 label_dn, self.txt_fld_dn,
                                                 label_em, self.txt_fld_em,
                                                 label_pw, self.txt_fld_pw,
                                                 sign_up_btn,
                                                 ft.Row([sign_in_lb, sign_in_vw],
                                                        alignment=ft.MainAxisAlignment.CENTER)],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                      expand=True,
                                      padding=170,
                                      bgcolor=ft.colors.BLUE_GREY_50,
                                      )

        # Main Row:
        row = ft.Row([heading_column, description],
                     alignment=ft.MainAxisAlignment.SPACE_EVENLY)

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
                color="#276749",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            ))

    # Client Side Validation:
    def validate(self):

        # Validate
        cs_valid_dn, cs_valid_em, cs_valid_pw = False, False, False

        # Check Display Name:
        display_name = self.txt_fld_dn.value

        if not (display_name.isalnum()) or not (6 <= len(display_name) <= 15):
            self.txt_fld_dn.error_text = "Display name should only be Alpha-numeric, 6-15 character long"
        else:
            cs_valid_dn, self.txt_fld_dn.error_text = True, ""

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
        if cs_valid_dn and cs_valid_em and cs_valid_pw:

            response = self.controller.sign_up_validation(display_name, email, password)

            # If signup was successful:
            if response == "200":
                self.controller.change_route("/verification")

            # Raise Error:
            else:
                self.txt_em.value = response
                self.txt_em.visible = True

        # Update page:
        self.controller.page.update()

    # Return View:
    def get_view(self):
        return ft.View(
            "/sign_up",
            controls=[self.main_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# if __name__ == "__main__":
#     ft.app(target=view)
