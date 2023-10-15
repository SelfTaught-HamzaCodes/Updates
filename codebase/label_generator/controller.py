from label_generator.model import Model

from label_generator.Views import Sign_up
from label_generator.Views import Email_verification
from label_generator.Views import Sign_in
from label_generator.Views import File_uploads
from label_generator.Views import Generate_labels
from label_generator.Views import Feedback
from label_generator.Views import Trail_Expired
from label_generator.Views import Forget_password


class Controller:
    def __init__(self, root):

        # Instances:
        self.page = root

        # Model Instance:
        self.model = Model()

        self.page.icon = "Logo.ico"

        # Views Instance:
        self.view1 = Sign_up.SignUp(self)
        self.view2 = Email_verification.EmailVerification(self)
        self.view3 = Sign_in.SignIn(self)
        # self.view4 = Welcome.Welcome(self)
        self.view5 = File_uploads.FileUploads(self)
        self.view6 = Generate_labels.GenerateLabels(self)
        self.view7 = Feedback.Feedback(self)
        self.view8 = Trail_Expired.TrailExpired(self)
        self.view9 = Forget_password.ForgetPassword(self)

        # Title:
        self.page.title = "Labelify"

        # Page (Minimum) Dimensions:
        self.page.window_min_width, self.page.window_min_height = 1280, 720

        # Full Screen Application:
        self.page.window_maximized = True

        # Initial Launch:
        self.launch = 0

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

        if not self.launch:
            session_validate = self.model.validate_session(self.launch)

            if session_validate == "Login":
                self.page.views.append(self.view3.get_view())

            elif session_validate == "Feedback":
                self.page.views.append(self.view7.get_view())

            elif session_validate == "Welcome":
                self.page.views.append(self.view5.get_view())

            elif session_validate == "Trail_Expired":
                self.page.views.append(self.view8.get_view())

            self.launch = 1

        # Add (Conditionals) Views:
        if self.page.route == "/sign_up":
            self.page.views.append(self.view1.get_view())

        if self.page.route == "/verification":
            self.page.views.append(self.view2.get_view())

        if self.page.route == "/sign_in":
            self.page.views.append(self.view3.get_view())

        # if self.page.route == "/welcome":
        #     self.page.views.append(self.view4.get_view())
        #     self.view4.animate()

        if self.page.route == "/file_uploads":
            self.page.views.append(self.view5.get_view())

        if self.page.route == "/generate_labels":
            self.page.views.append(self.view6.get_view())

        if self.page.route == "/feedback":
            self.page.views.append(self.view7.get_view())

        if self.page.route == "/trail_expired":
            self.page.views.append(self.view8.get_view())

        if self.page.route == "/forget_password":
            self.page.views.append(self.view9.get_view())

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    # Server side validation for user-credentials on (Sign Up):
    def sign_up_validation(self, display_name, email, password):

        # Pass Credentials to Model:
        return self.model.sign_up(display_name, email, password)

    # Server side validation for user-credentials on (Sign In):
    def sign_in_validation(self, email, password, remember):

        # Pass Credentials to Model:
        return self.model.sign_in(email, password, remember)

    # Logout:
    def logout(self):

        self.model.logout()

        self.change_route("/sign_in")

    # Get display name from JSON file:
    def get_display_name(self):

        # Get display name:
        return self.model.read_data(self.model.get_local_file("session.json")["display_name"])

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

    # Get Fixed Values:
    def get_fixed_values(self, placeholder):

        return self.model.get_fixed_values(placeholder)

    # Set Feedback:
    def set_feedback(self, rating, likes, dislikes, updates, feedback):

        return self.model.set_feedback(rating, likes, dislikes, updates, feedback)
