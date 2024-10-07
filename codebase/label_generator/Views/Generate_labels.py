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


        # DataTable:
        self.datatable = ft.DataTable(

            columns=[
                ft.DataColumn(ft.Text("PlaceHolders", font_family="arvo", color=ft.colors.WHITE)),
                ft.DataColumn(ft.Text("Select Value", font_family="arvo", color=ft.colors.WHITE)),
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
            ft.Row([heading], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([generate], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.file_uploads, self.generate_label], alignment=ft.MainAxisAlignment.CENTER)

        ], expand=True,alignment=ft.MainAxisAlignment.CENTER)

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

            print(placeholder)

            text_element = ft.Text(placeholder, font_family="arvo")
            dropdown_element = ft.Dropdown(border=ft.InputBorder.NONE,
                                           border_color="#1D976C",
                                           hint_text="Select Value",
                                           hint_style=ft.TextStyle(font_family="arvo"),
                                           options=[
                                               ft.dropdown.Option(option) for option in self.columns
                                           ])
           
            self.elements[placeholder] = {
                'text_element': text_element,
                'dropdown_element': dropdown_element,
            }

        self.datatable.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(element_values['text_element']),
                    ft.DataCell(element_values['dropdown_element']),
                    
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

    # Return View:
    def get_view(self):

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
