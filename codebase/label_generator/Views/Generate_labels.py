import flet as ft


class GenerateLabels:
    def __init__(self, controller):
        # Set Controller:
        self.controller = controller

        # Set Title and Alignments:
        self.controller.page.title = "Generate Labels"
        self.controller.page.bgcolor = ft.colors.BLUE_GREY_50

        self.controller.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.controller.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fonts:
        self.controller.page.fonts = {
            "arvo": self.controller.model.resource_path("Arvo-Regular.ttf")
        }

        # Set Minimum Window Size:
        self.controller.page.window_min_width, self.controller.page.window_min_height = 1280, 720

        # Placeholders & Columns:
        self.placeholders = []
        self.columns = []
        self.elements = {}

        # Generated Label:
        self.generated = None

        # File Picker:
        self.file_picker = ft.FilePicker(on_result=self.save_label)
        self.controller.page.overlay.append(self.file_picker)
        self.controller.page.update()

        # Heading:
        heading = ft.Text(
            value="Generate Label",
            style=ft.TextThemeStyle.HEADLINE_LARGE,
            weight=ft.FontWeight.W_500,
            font_family="arvo",
            color=ft.colors.BLUE_GREY_50)

        # Settings:
        self.display_name = None

        self.settings = ft.PopupMenuButton(
            content=ft.Icon(name=ft.icons.SETTINGS, color=ft.colors.BLUE_GREY_50),
        )

        # DataTable:
        self.datatable = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("PlaceHolders", font_family="arvo", color=ft.colors.WHITE)),
                ft.DataColumn(ft.Text("Fixed", font_family="arvo", color=ft.colors.WHITE)),
                ft.DataColumn(ft.Text("Select Value", font_family="arvo", color=ft.colors.WHITE, width=200)),
                ft.DataColumn(ft.Text("Enter Value", font_family="arvo", color=ft.colors.WHITE)),
                ft.DataColumn(ft.Text("Save Value", font_family="arvo", color=ft.colors.WHITE))

            ],
            heading_row_color="#1D976C",
            expand=True,
        )

        # DataTable Container:
        self.db_cont = ft.Container(
            content=ft.ListView(controls=[self.datatable]),
            border=ft.border.all(2, "#1D976C"),
            border_radius=5,
            width=640,
            height=530,
            expand=True,
            margin=5,
        )

        # File Uploads:
        self.file_uploads = ft.ElevatedButton(content=ft.Text("File Uploads", font_family="arvo"),
                                              width=160,
                                              color=ft.colors.WHITE,
                                              bgcolor="#1D976C",
                                              on_click=lambda _: self.controller.page.go("/file_uploads"),
                                              style=ft.ButtonStyle(
                                                  shape=ft.RoundedRectangleBorder(radius=15)
                                              ))

        # Generate - Popup:
        self.generate_label = ft.ElevatedButton(content=ft.Text("Generate", font_family="arvo"),
                                                width=160,
                                                color=ft.colors.WHITE,
                                                bgcolor="#1D976C",
                                                on_click=self.generate_label,
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=15)
                                                ))

        # CONTAINERS

        # DataTable, Placement:
        datatable_placement = ft.Column(
            [
                ft.Row([self.db_cont], alignment=ft.MainAxisAlignment.CENTER),

            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )

        # Container:
        generate = ft.Container(
            content=ft.Row([datatable_placement]),
            width=960,
            height=540,
            border_radius=5,
            margin=ft.margin.only(top=25, left=250, right=250),
            bgcolor=ft.colors.WHITE,
            expand=True,
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["WHITE", ft.colors.BLUE_GREY_100]
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="#1D976C",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.NORMAL,
            )
        )

        # Container B:
        positioning = ft.Column([
            ft.Row([self.settings]),
            ft.Row([heading], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([generate], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.file_uploads, self.generate_label], alignment=ft.MainAxisAlignment.CENTER)

        ], expand=True)

        # Main Container:
        self.outer_container = ft.Container(
            ft.Row([positioning]),
            expand=True,
            bgcolor="#004643",
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1D976C", "#93F9B9"]
            ))

    # Load Datable:
    def load_datatable(self):

        # Reset rows and elements:
        self.datatable.rows.clear()
        self.elements.clear()

        # Add Elements:
        for placeholder in self.placeholders:
            text_element = ft.Text(placeholder, font_family="arvo")
            checkbox_element = ft.Checkbox(fill_color="#1D976C")
            dropdown_element = ft.Dropdown(border=ft.InputBorder.NONE,
                                           border_color="#1D976C",
                                           hint_text="Select Value",
                                           hint_style=ft.TextStyle(font_family="arvo"),
                                           options=[
                                               ft.dropdown.Option(option) for option in self.columns
                                           ])
            text_field_element = ft.TextField(hint_text="Enter Value",
                                              disabled=True,
                                              border=ft.InputBorder.NONE,
                                              text_style=ft.TextStyle(font_family="arvo"))

            save_checkbox = ft.Checkbox(fill_color="#1D976C", disabled=True)

            checkbox_element.on_change = lambda _, p=placeholder: self.checkbox_dynamic(p)

            self.elements[placeholder] = {
                'text_element': text_element,
                'checkbox_element': checkbox_element,
                'dropdown_element': dropdown_element,
                'text_field_element': text_field_element,
                'save_checkbox': save_checkbox,
            }

        self.datatable.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(element_values['text_element']),
                    ft.DataCell(element_values['checkbox_element']),
                    ft.DataCell(element_values['dropdown_element']),
                    ft.DataCell(element_values['text_field_element']),
                    ft.DataCell(element_values['save_checkbox'])

                ]
            ) for element_values in self.elements.values()
        ]

    # Generate Label:
    def generate_label(self, e):

        # Ask Controller to Generate Label Documents:
        self.generated = self.controller.generate_label_doc(self.elements)

        # Path to save file:
        self.file_picker.save_file(
            allowed_extensions=['docx'],
        )

    def save_label(self, e: ft.FilePickerResultEvent):

        # Save Label

        path = e.path + ".docx"

        self.generated.save(path)

    # Change Fixed / Non-Fixed Checkbox:
    def checkbox_dynamic(self, placeholder):

        # Checkbox value:
        cb_value = self.elements[placeholder]["checkbox_element"].value

        # If fixed values:
        if cb_value:

            # Value for Text-Field:
            self.elements[placeholder]["text_field_element"].disabled = False
            self.elements[placeholder]["text_field_element"].value = ""
            self.elements[placeholder]["save_checkbox"].disabled = False

            # Load values from JSON:
            self.elements[placeholder]["dropdown_element"].options = [
                ft.dropdown.Option(option) for option in self.controller.get_fixed_values(placeholder)
            ]

        else:

            # Value for Drop-Down:
            self.elements[placeholder]["dropdown_element"].value = ""
            self.elements[placeholder]["dropdown_element"].options = [
                ft.dropdown.Option(option) for option in self.columns
            ]

            # Disable Text Field and Checkbox:
            self.elements[placeholder]["text_field_element"].value = ""
            self.elements[placeholder]["text_field_element"].disabled = True
            self.elements[placeholder]["save_checkbox"].value = False
            self.elements[placeholder]["save_checkbox"].disabled = True

        self.controller.page.update()

    # Display Name:
    def get_display_name(self):

        json_file = self.controller.model.get_local_file("session.json")

        session = self.controller.model.decrypt_file(json_file, self.controller.model.generate_key(),
                                                     retrieve=True)
        self.display_name = session["display_name"]

        self.settings.items = [
            ft.PopupMenuItem(text=F"Hi, {self.display_name}", icon=ft.icons.ACCOUNT_CIRCLE),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(text="Check for updates", icon=ft.icons.UPDATE, on_click=lambda _:self.check_update()),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(text="Logout", icon=ft.icons.LOGOUT, on_click=lambda _:self.controller.logout())
        ]

    # Update check:
    def check_update(self):

        # Current version:
        application = self.controller.model.application_version()

        # Check for updates:
        update_available = self.controller.model.update_available()

        download_link = ft.Text()

        # Link to download (if update is available):
        if update_available == "Update available":
            download_link = ft.Text(spans=[ft.TextSpan(
                "Click to Download Update!", ft.TextStyle(color="#1D976C", weight=ft.FontWeight.BOLD),
                url="https://github.com/SelfTaught-HamzaCodes/Labelify",
            )], color="#1D976C", font_family="arvo", style=ft.TextThemeStyle.TITLE_MEDIUM)

        # Placement:
        content = ft.Column([
            ft.Row([ft.Text(f"Current Version: ", spans=[ft.TextSpan(
                f"{application}", ft.TextStyle(color="#1D976C", weight=ft.FontWeight.BOLD)
            )], color="#1D976C", font_family="arvo", style=ft.TextThemeStyle.TITLE_MEDIUM)]),

            ft.Row([ft.Text(f"Status: ", spans=[ft.TextSpan(
                f"{update_available}", ft.TextStyle(color="#1D976C", weight=ft.FontWeight.BOLD)
            )], color="#1D976C", font_family="arvo", style=ft.TextThemeStyle.TITLE_MEDIUM)]),

            ft.Row([download_link])

        ], height=75)

        self.dialog_x = ft.AlertDialog(
            title=ft.Text("Application Updates", font_family="arvo", color="#004643"),
            content=content,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            open=False)

        # Open AlertDialog:
        self.controller.page.dialog = self.dialog_x
        self.dialog_x.open = True
        self.controller.page.update()

    # Return View:
    def get_view(self):

        # Display Name:
        self.get_display_name()

        # Get PlaceHolders:
        self.placeholders = self.controller.get_placeholders()

        # Get Column Names:
        self.columns = self.controller.get_column_names()

        self.load_datatable()

        return ft.View(
            "/generate_labels",
            controls=[self.outer_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
