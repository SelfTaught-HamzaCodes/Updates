from label_generator.model import Model

from label_generator.Views import File_uploads
from label_generator.Views import Generate_labels


class Controller:
    def __init__(self, root):

        # Instances:
        self.page = root

        # Model Instance:
        self.model = Model()

        self.page.icon = "Logo.ico"

        # Views Instance:
        self.view5 = File_uploads.FileUploads(self)
        self.view6 = Generate_labels.GenerateLabels(self)

        # Title:
        self.page.title = "Labelify"

        # Page (Minimum) Dimensions:
        self.page.window_min_width, self.page.window_min_height = 1280, 720

        # Full Screen Application:
        self.page.window_maximized = True

        # Change routes:
        self.route_change(self.page.route)

    def change_route(self, route):
        """
        Helper method to change views, within a function of a view.
        """

        self.page.route = route

        # Change routes:
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def route_change(self, route):
        self.page.views.clear()

        self.page.views.append(self.view5.get_view())

        if self.page.route == "/file_uploads":
            self.page.views.append(self.view5.get_view())

        if self.page.route == "/generate_labels":
            self.page.views.append(self.view6.get_view())

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    # Set Excel and its configuration settings:
    def set_excel_values(self, excel, sheet, row):

        self.model.set_excel_values(excel, sheet, row)

    # Get Excel and its configuration settings:
    def get_excel_values(self):

        return self.model.get_excel_values()

    # Get Column Names:
    def get_column_names(self):

        return self.model.get_column_names()

    # Set Excel and its configuration settings:
    def set_word_file(self, word):

        self.model.set_word_file(word)

    # Get Excel and its configuration settings:
    def get_word_file(self):

        return self.model.get_word_file()

    # Get Placeholders:
    def get_placeholders(self):

        return self.model.get_placeholders()

    # Generate Label Documents:
    def generate_label_doc(self, elements):

        return self.model.generate_label_doc(elements)

