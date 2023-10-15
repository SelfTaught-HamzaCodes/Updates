import flet as ft


class Feedback:
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

        # Feedback Variables:
        self.rating = 0
        self.likes = []
        self.dislikes = []
        self.updates = []
        self.feedback_message = ""

        # Main Heading:
        heading = ft.Text("Your Feedback Matters: A Quick Questionnaire",
                          color="#1D976C",
                          font_family="arvo",
                          weight=ft.FontWeight.W_800,
                          style=ft.TextThemeStyle.HEADLINE_LARGE)

        # Question: 1
        question_one = ft.Text("How satisfied are you with this application ?",
                               font_family="arvo",
                               weight=ft.FontWeight.W_800,
                               style=ft.TextThemeStyle.TITLE_MEDIUM)

        # Store Buttons:
        self.buttons = {}

        for rate in range(1, 6):
            button = ft.ElevatedButton(content=ft.Text(str(rate), font_family="arvo", color="#1D976C"),
                                       bgcolor=ft.colors.WHITE,
                                       on_click=lambda _, p=rate: self.satisfaction(p),
                                       style=ft.ButtonStyle(
                                           shape=ft.RoundedRectangleBorder(radius=5)
                                       ))

            self.buttons[rate] = button

        button_placement = ft.Row([button for button in self.buttons.values()])

        # Question: 2
        like_options = ["Ease of use", "Responsiveness", "File Uploads", "Label Formats", "Design", "None"]

        dictionary_likes = {}

        for like in like_options:
            # Text Field:
            text = ft.Text(like, font_family="arvo")

            # Checkbox for Likes:
            checkbox_like = ft.Checkbox(fill_color="#1D976C")
            checkbox_like.on_change = lambda _, p=like, q=checkbox_like: self.preferences(p, q, "likes")

            # Checkbox for Dislikes:
            checkbox_d_like = ft.Checkbox(fill_color="#1D976C")
            checkbox_d_like.on_change = lambda _, p=like, q=checkbox_d_like: self.preferences(p, q, "dislikes")

            # Add values to Dictionary:
            dictionary_likes[like] = [text, checkbox_like, checkbox_d_like]

        like_database = ft.Container(ft.ListView([ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Features", font_family="arvo", color=ft.colors.BLUE_GREY_50)),
                ft.DataColumn(ft.Text("Like", font_family="arvo", color=ft.colors.BLUE_GREY_50)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(value[0]),
                    ft.DataCell(value[1])
                ])
                for value in dictionary_likes.values()],
            heading_row_color="#1D976C")],
            height=150),
            border_radius=5,
            border=ft.border.all(color="#1D976C"))

        dislike_database = ft.Container(ft.ListView([ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Features", font_family="arvo", color=ft.colors.WHITE)),
                ft.DataColumn(ft.Text("Dislike", font_family="arvo", color=ft.colors.WHITE))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(value[0]),
                    ft.DataCell(value[2])
                ])
                for value in dictionary_likes.values()],
            heading_row_color="#1D976C",
        )]),
            height=150,
            border_radius=5,
            border=ft.border.all(color="#1D976C")
        )

        update_options = ["Language Support", "Auto-Fill Values", "Free Versions", "Preset Labels", "None"]

        dictionary_update = {}

        for update in update_options:
            text = ft.Text(update, font_family="arvo")
            checkbox_like = ft.Checkbox(fill_color="#1D976C")

            checkbox_like.on_change = lambda _, p=update, q=checkbox_like: self.preferences(p, q, "updates")

            dictionary_update[update] = [text, checkbox_like]

        update_datatable = ft.Container(ft.ListView([ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Features", font_family="arvo", color=ft.colors.BLUE_GREY_50)),
                ft.DataColumn(ft.Text("Update", font_family="arvo", color=ft.colors.BLUE_GREY_50)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(value[0]),
                    ft.DataCell(value[1])
                ])
                for value in dictionary_update.values()],
            heading_row_color="#1D976C",
        )]),
            height=150,
            border_radius=5,
            border=ft.border.all(color="#1D976C")
        )

        #
        like = ft.Column([
            ft.Text("Features you found the most useful ?",
                    font_family="arvo",
                    style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.W_800),
            like_database
        ], expand=True)

        dislike = ft.Column([
            ft.Text("Features you found difficult to navigate ?",
                    font_family="arvo",
                    style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.W_800),
            dislike_database
        ], expand=True)

        update = ft.Column([
            ft.Text("Features you would like see an update ?",
                    font_family="arvo",
                    style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.W_800),
            update_datatable
        ], expand=True)

        # Question: 3
        question_two = ft.Text("Leave a feedback for improvements",
                               font_family="arvo",
                               style=ft.TextThemeStyle.TITLE_MEDIUM,
                               weight=ft.FontWeight.W_800)

        self.feedback = ft.TextField(label="Enter your feedback",
                                     multiline=True,
                                     min_lines=1,
                                     max_lines=5,
                                     text_style=ft.TextStyle(font_family="arvo"),
                                     label_style=ft.TextStyle(color="#1D976C", font_family="arvo")
                                     )

        # Placement of Feedback:
        feedback_container = ft.Container(
            content=self.feedback,
            expand=True, padding=ft.padding.only(left=200, right=200)
        )

        # Error Messages:
        self.error = ft.Text(visible=False,
                             font_family="arvo",
                             style=ft.TextThemeStyle.LABEL_MEDIUM,
                             color=ft.colors.RED_500)

        # Submit Feedback:
        submit_feedback = ft.ElevatedButton(
            content=ft.Text("Submit Feedback", font_family="arvo", color=ft.colors.BLUE_GREY_50),
            bgcolor="#1D976C",
            on_click=self.record_feedback,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            ))

        # Placement for Body:
        body_container = ft.Column([
            ft.Row([heading], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([question_one], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([button_placement], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([like, dislike, update], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([question_two], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([feedback_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(thickness=2),
            ft.Row([self.error], alignment=ft.MainAxisAlignment.CENTER),
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
                color="#1D976C",
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.NORMAL
            ),
            margin=100,
            # margin=ft.margin.only(top=100,
            #                       bottom=200,
            #                       left=200,
            #                       right=200),
            padding=20,
        )

        # # Main Container:
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
            content=ft.Column([body], alignment=ft.MainAxisAlignment.CENTER),
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1D976C", "#93F9B9"]
            )
        )

    def preferences(self, t_control, cb_control, preference_type):

        if preference_type == "likes":

            # If selected:
            if cb_control.value:
                self.likes.append(t_control)

            else:
                self.likes.remove(t_control)

        elif preference_type == "dislikes":

            # If selected:
            if cb_control.value:
                self.dislikes.append(t_control)

            else:
                self.dislikes.remove(t_control)

        elif preference_type == "updates":

            # If selected:
            if cb_control.value:
                self.updates.append(t_control)

            else:
                self.updates.remove(t_control)

    def satisfaction(self, rating):

        # Change previous button to default color:
        for key, button in self.buttons.items():
            if key != rating:
                button.bgcolor = ft.colors.WHITE

        # Change selected button to new color:
        self.buttons[rating].bgcolor = ft.colors.GREEN_200

        # Set Rating:
        self.rating = rating

        self.controller.page.update()

    def record_feedback(self, e):

        # Check if feedback form is filled:
        if self.rating == 0:
            self.show_error("Select a rating for the application.")
            return False

        if not self.likes:
            self.show_error("Select a feature you liked, you can select None.")
            return False

        if not self.dislikes:
            self.show_error("Select a feature you disliked, you can select None.")
            return False

        if not self.updates:
            self.show_error("Select a feature you would like an update on, you can select None.")
            return False

        # Values are filled, remove the error messages:
        self.error.visible = False
        self.controller.page.update()

        # Check Message Feedback (if any):
        self.feedback_message = self.feedback.value

        # Set Feedback:
        response = self.controller.set_feedback(self.rating, self.likes, self.dislikes, self.updates,
                                                self.feedback_message)

        # Success:
        if response == "200":

            # Check if newly log in user has given the feedback:
            view = self.controller.model.validate_session(self.controller.launch)

            if view == "Welcome":
                self.controller.change_route("/file_uploads")

            elif view == "Trail_Expired":
                self.controller.change_route("/trail_expired")

        # Not Success:
        else:
            self.show_error(response)

    def show_error(self, prompt):

        self.error.value = prompt
        self.error.visible = True
        self.controller.page.update()

    # Return View:
    def get_view(self):

        return ft.View(
            "/feedback",
            controls=[self.oc],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
