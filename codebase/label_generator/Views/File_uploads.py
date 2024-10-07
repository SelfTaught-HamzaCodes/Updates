import flet as ft
import pandas as pd
import os


class FileUploads:
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

        # File Picker:
        file_picker = ft.FilePicker(on_result=self.file_processing)
        self.controller.page.overlay.append(file_picker)
        self.controller.page.update()

        # Dialog:
        self.dialog_x = None

        # Excel Sheets:
        self.excel_sheets = None

        
        # Icons:

        # Excel:
        excel_icon = ft.Icon(ft.icons.UPLOAD_FILE_ROUNDED, color="#1D976C", size=40)

        # Word:
        word_icon = ft.Icon(ft.icons.UPLOAD_FILE_ROUNDED, color="#1D6D97", size=40)

        # Buttons:

        # Excel:
        excel_button = ft.ElevatedButton(content=ft.Text("Upload Packing List", font_family="arvo"),
                                         color=ft.colors.WHITE,
                                         width=300,
                                         bgcolor="#1D976C",
                                         on_click=lambda _: file_picker.pick_files(allow_multiple=False,
                                                                                   allowed_extensions=["xlsx"]),
                                         style=ft.ButtonStyle(
                                             shape=ft.RoundedRectangleBorder(radius=15)
                                         ))

        # Word:
        word_button = ft.ElevatedButton(content=ft.Text("Upload Label Format", font_family="arvo"),
                                        color=ft.colors.WHITE,
                                        width=300,
                                        bgcolor="#1D6D97",
                                        on_click=lambda _: file_picker.pick_files(allow_multiple=False,
                                                                                  allowed_extensions=["docx"]),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=15)
                                        ))

        # Supported Formats:

        # Excel:
        excel_sf = ft.Text(
            "Supported Formats: ",
            spans=[
                ft.TextSpan(
                    "xlsx",
                    ft.TextStyle(color="#1D976C",
                                 weight=ft.FontWeight.W_500),
                )
            ],
            style=ft.TextThemeStyle.LABEL_MEDIUM,
            color=ft.colors.GREY_500)

        # Word:
        word_sf = ft.Text(
            "Supported Formats: ",
            spans=[
                ft.TextSpan(
                    "docx",
                    ft.TextStyle(color="#1D6D97",
                                 weight=ft.FontWeight.W_500),
                )
            ],
            style=ft.TextThemeStyle.LABEL_MEDIUM,
            color=ft.colors.GREY_500)

        # Upload File Name:

        # Excel:
        self.excel_f = ft.TextField(
            label="File Selected",
            border=ft.InputBorder.NONE,
            filled=True,
            bgcolor="#1D976C",
            text_style=ft.TextStyle(font_family="arvo", color="WHITE"),
            label_style=ft.TextStyle(font_family="arvo", color="white"),
            disabled=True,
        )

        # Word:
        self.word_f = ft.TextField(
            label="File Selected",
            border=ft.InputBorder.NONE,
            bgcolor="#1D6D97",
            text_style=ft.TextStyle(font_family="arvo", color="WHITE"),
            label_style=ft.TextStyle(font_family="arvo", color="white"),
            disabled=True,
            filled=True,
        )

        # Heading - Container A-A:
        heading = ft.Text(
            value="Upload Files",
            style=ft.TextThemeStyle.HEADLINE_LARGE,
            weight=ft.FontWeight.W_500,
            font_family="Arvo",
            color=ft.colors.BLUE_GREY_50)

        # Placement:

        # Excel:

        excel_placement = ft.Column([
            ft.Row([excel_icon], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([excel_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([excel_sf], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.excel_f], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Word:
        word_placement = ft.Column([
            ft.Row([word_icon], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([word_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([word_sf], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.word_f], alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Button:
        self.generate = ft.ElevatedButton(content=ft.Text("Generate", font_family="arvo"),
                                          disabled=True,
                                          width=250,
                                          color=ft.colors.BLUE_GREY_900,
                                          bgcolor="#1D976C",
                                          on_click=lambda _: self.controller.change_route("/generate_labels"),
                                          style=ft.ButtonStyle(
                                              shape=ft.RoundedRectangleBorder(radius=5)
                                          ))

        # CONTAINERS

        # Container A-B - Excel:
        excel_container = ft.Container(
            excel_placement,
            width=480,
            height=270,
            border_radius=5,
            margin=10,
            bgcolor=ft.colors.WHITE,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["white", ft.colors.BLUE_GREY_100]
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#1D976C",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.NORMAL,
            )
        )

        # Container A-C - Word:
        word_container = ft.Container(
            word_placement,
            width=480,
            height=270,
            border_radius=5,
            margin=10,
            bgcolor=ft.colors.WHITE,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["white", ft.colors.BLUE_GREY_100]
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
            ft.Row([excel_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([word_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self.generate], alignment=ft.MainAxisAlignment.CENTER)
        ], expand=True, alignment=ft.MainAxisAlignment.CENTER)

        # Main Container:
        self.outer_container = ft.Container(
            content=ft.Row([positioning], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            bgcolor="#004643",
            margin=0,
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1D976C", "#93F9B9"]
            ))

    # File processing:
    def file_processing(self, e: ft.FilePickerResultEvent):

        # Determine File Type:
        try:
            file_name, extension = os.path.splitext(e.files[0].path)
            # Excel Extension:
            if extension == ".xlsx":

                # Create dataframe for excel:
                excel_df = pd.ExcelFile(os.path.join(e.files[0].path))

                # Extract Sheets:
                self.excel_sheets = excel_df.sheet_names

                # Content For Dialog:
                self.sheet = ft.Dropdown(
                    label="Select Sheet",
                    label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
                    hint_text="Select sheet with details.",
                    hint_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
                    options=[ft.dropdown.Option(column) for column in self.excel_sheets]
                )

                self.rows = ft.Dropdown(
                    label="Select Row",
                    label_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
                    hint_text="Select rows with headings.",
                    hint_style=ft.TextStyle(font_family="arvo", color="#1D976C"),
                    options=[ft.dropdown.Option(x) for x in range(1, 11)]
                )

                self.placing = ft.Column(
                    [self.sheet, self.rows],
                    alignment=ft.MainAxisAlignment.CENTER
                    , height=250)

                # Show pop-up:
                self.dialog_x = ft.AlertDialog(
                    title=ft.Text("Configure Excel",
                                  font_family="arvo",
                                  color="#1D976C"),
                    content=self.placing,
                    actions=[
                        ft.ElevatedButton(content=ft.Text("Done", font_family="arvo"),
                                          color=ft.colors.WHITE,
                                          width=300,
                                          bgcolor="#1D976C",
                                          on_click=lambda _: self.set_excel_values(
                                              e.files[0].path, self.sheet.value, self.rows.value
                                          ))
                    ],
                    actions_alignment=ft.MainAxisAlignment.CENTER,
                    open=False,
                    # on_dismiss=lambda _: self.set_excel_values(
                    #     None, None, None
                    # )
                )
                
                
                self.excel_f.value = e.files[0].name

                # Open AlertDialog:
                self.controller.page.dialog = self.dialog_x
                self.dialog_x.open = True
                self.controller.page.update()

            # Word Extension:
            elif extension == ".docx":
                self.controller.set_word_file(e.files[0].path)
                self.word_f.value = e.files[0].name
                self.controller.page.update()


            # Error:
            else:
                print("Invalid Extension")

            # Enable Button, if both files are selected:
            if all(self.controller.get_excel_values()) and self.controller.get_word_file():
                self.generate.disabled = False
                self.generate.bgcolor=ft.colors.BLUE_GREY_50
                self.controller.page.update()

        except Exception as f:
            print(f)
            return False

    # Set Values:
    def set_excel_values(self, path, sheet, row):

        # Close Dialog Box:
        self.dialog_x.open = False
        self.controller.page.update()

        # Pick Defaults:
        if not self.sheet.value:
            sheet = self.excel_sheets[0]

        if not self.rows.value:
            row = 1

        # Set Excel Values:
        self.controller.set_excel_values(path, sheet, row)

    # Return View:
    def get_view(self):

        # Reset Placeholders:
        self.controller.model.placeholders.clear()

        return ft.View(
            "/file_uploads",
            controls=[self.outer_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
