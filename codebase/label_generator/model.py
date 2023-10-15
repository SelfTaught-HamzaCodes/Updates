# Model for application, Data Storage and Communications with API.

import textract
import re
import os
import sys
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Local Storage:
import json

# Imports to Generate Label Document:
from docx import Document
from docxtpl import DocxTemplate
from lxml import etree

# Security:
from cryptography.fernet import Fernet
import hashlib

# Requests
import requests

load_dotenv()


class Model:
    def __init__(self):

        # Set Client:
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")

        self.supabase = create_client(self.url, self.key)
        self.user = None

        # Create Local Files:
        self.create_local_files()

        # Initialise the paths for Excel (Configurations) and Word Files:
        self.excel_path = None
        self.excel_sheet = None
        self.excel_row = None

        self.word_path = None
        self.placeholders = []

    # Get abs_path to source:
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def create_local_files():
        """
        Creates local files specific to each user.
        """

        # Local Files:
        files = ["session.json", "session.key", "session_hash.key", "fixed.json", "config.json"]

        # Get the user's APPDATA directory
        user_dir = os.path.join(os.environ['APPDATA'], "Label Generator")

        # Create the base directory if it doesn't exist
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        # Specify the file path:
        for file_ in files:
            file_path = os.path.join(user_dir, file_)

            # Create the file if it doesn't exist
            if not os.path.exists(file_path):

                if file_.endswith(".key"):
                    # Create an empty key file by opening it in binary write mode
                    with open(file_path, 'wb'):
                        pass  # This creates an empty binary file
                else:
                    # For other files, create empty JSON files
                    with open(file_path, 'w') as file:
                        file.write('{"version": "0.1"}') if file_ == "config.json" else file.write('{}')

    @staticmethod
    def get_local_file(file_path):

        user_dir = os.path.join(os.environ['APPDATA'], "Label Generator")

        return os.path.join(user_dir, file_path)

    # Communicate with the Supabase Authentication for Sign Up:
    def sign_up(self, display_name, email, password):

        try:
            # Call Supabase authentication API to sign up the user:
            self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {"display_name": display_name,
                             "feedback_recorded": 0}
                }
            })

            # Add email as a key to fixed.json:
            fixed = self.get_local_file("fixed.json")

            fixed_json = self.read_data(fixed)

            if not fixed_json.get(email, 0):
                fixed_json[email] = {}

            self.write_data(fixed, fixed_json)

            # If no exceptions are raised above:
            return "200"  # Success

        except Exception as e:
            return e

    # Communicate with the Supabase Authentication for Sign In:
    def sign_in(self, email, password, remember):

        try:
            # Call Supabase authentication API to sign in the user:
            self.user = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password})

            # JSON file path:
            session = self.get_local_file("session.json")

            # Try to decrypt:
            try:
                # Try to decrypt file, using the key:
                self.decrypt_file(session, self.generate_key())

            except Exception:
                pass

            # Read Data:
            stored_data = self.read_data(session)

            # Modify data:
            stored_data["email"] = email
            stored_data["created_at"] = self.user.user.created_at.date().isoformat()
            stored_data["display_name"] = self.user.user.user_metadata["display_name"]

            # Feedback Recorded:
            stored_data["feedback_recorded"] = 1 if self.supabase.table('Feedback').select("email").eq("email",
                                                                                                       email).execute().data else 0

            stored_data["remember_me"] = 1 if remember else 0

            # Write data:
            self.write_data(session, stored_data)

            # Generate new hash value:
            self.get_hash(update=True)

            # Encrypt data:
            self.encrypt_file(session, self.generate_key())

            # If no exceptions are raised above:
            return "200"  # Success

        except Exception as e:
            return e

    # Logout:
    def logout(self):

        session = self.get_local_file("session.json")

        # Try to decrypt:
        try:
            # Try to decrypt file, using the key:
            self.decrypt_file(session, self.generate_key())

        except Exception:
            pass

        session_read = self.read_data(session)

        # Change remember me to False:
        session_read["remember_me"] = 0

        # Write new changes:
        self.write_data(session, session_read)

        # Generate new hash:
        self.get_hash(update=True)

        # Encrypt data:
        self.encrypt_file(session, self.generate_key())

    # Validate Session
    def validate_session(self, initial):

        session = self.get_local_file("session.json")

        # Try to decrypt:
        try:
            # Try to decrypt file, using the key:
            self.decrypt_file(session, self.generate_key())

        except Exception:
            pass

        # Read Data:
        session_data = self.read_data(session)

        # Check if user selected Remember Me, after login initial is True, need to also check if any tempering:
        if (session_data.get("remember_me", 0) or initial) and self.is_file_tampered(session, self.get_hash()):

            # Check if user has passed 14 days and feedback is not recorded:
            trail_used = session_data["created_at"]

            # Convert the stored date back to a datetime.date object
            stored_date = datetime.strptime(trail_used, "%Y-%m-%d").date()

            # Calculate the difference between today's date and the stored date
            current_date = datetime.now().date()
            date_difference = current_date - stored_date

            # Extract the number of days from the date difference
            number_of_days = date_difference.days

            # If 14 days have passed, and the feedback isn't recorded:
            if number_of_days >= 14 and not session_data["feedback_recorded"]:

                # Prompt for Feedback:
                # Encrypt data:
                self.encrypt_file(session, self.generate_key())
                return "Feedback"

            # Feedback recorded, and number of days within trail:
            elif number_of_days <= 30:

                # Prompt for Welcome:
                self.encrypt_file(session, self.generate_key())
                return "Welcome"

            # Trial expired:
            else:

                # Prompt for Trial Expired:
                self.encrypt_file(session, self.generate_key())
                return "Trail_Expired"

        else:

            # Prompt Login
            return "Login"

    # Send OTP:
    def send_otp(self, email):
        try:
            self.supabase.auth.reset_password_email(email, options={".Token": True})

            # Success:
            return "200"

        except Exception as e:
            return e

    # Validate OTP:
    def validate_otp(self, email, token):
        try:
            self.user = self.supabase.auth.verify_otp({"email": email, "token": token, "type": "email"})

            # Return success:
            return "200"

        except Exception as e:
            return e

    # Change password:
    def change_password(self, password):
        try:
            self.supabase.auth.update_user({"password": password})

            # Success:
            return "200"

        except Exception as e:
            return e

    # Read JSON files:
    @staticmethod
    def read_data(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # Write JSON files:
    @staticmethod
    def write_data(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file)

    # Get Hash of Original File:
    def get_hash(self, update=False):
        """
        Generates a key and stores it (if it doesn't exist), returns Key.
        """

        session = self.get_local_file("session.json")
        hash_key = self.get_local_file("session_hash.key")

        # If key exists, or an updated key is not requested:
        if os.path.exists(hash_key) and not update:
            with open(hash_key, "rb") as session_key:

                # Reads and returns the key.
                return session_key.read().decode()

        else:

            # Try to decrypt:
            try:
                # Try to decrypt file, using the key:
                self.decrypt_file(session, self.generate_key())

            except Exception:
                pass

            # Generate Key:
            hash_value = self.calculate_hash(session)

            # Store Key:
            with open(hash_key, "wb") as session_key:
                session_key.write(hash_value.encode())

            return hash_value

    # Calculate Hash Value, of a given file:
    @staticmethod
    def calculate_hash(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()

    # Compare Hash Values:
    def is_file_tampered(self, file_path, stored_hash):

        current_hash = self.calculate_hash(file_path)
        return current_hash == stored_hash

    # Generate Key:
    def generate_key(self):
        """
        Generates a key and stores it (if it doesn't exist), returns Key.
        """

        key_file = self.get_local_file("session.key")

        # If key exists:
        with open(key_file, "rb") as session_key:

            key = session_key.read()

            if key:
                # Reads and returns the key.
                return key

            else:
                # Generate Key:
                key = Fernet.generate_key()

                # Store Key:
                with open(key_file, "wb") as session_key_file:
                    session_key_file.write(key)

                return key

    # Encrypt File:
    def encrypt_file(self, file, key):
        """
        Encrypts a file using a key.
        """

        file = self.get_local_file(file)

        with open(file, "rb") as session_read:
            # Load JSON data
            json_data = json.load(session_read)

            # Encrypt JSON data
            encrypted = Fernet(key).encrypt(json.dumps(json_data).encode('utf-8'))

        with open(file, "wb") as session_write:
            # Replace original JSON data with encrypted content
            session_write.write(encrypted)

    def decrypt_file(self, file, key, retrieve=False):
        """
        Decrypts a file using a key, and return the file.
        """

        file = self.get_local_file(file)

        if not retrieve:
            with open(file, "rb") as session_read:
                decrypted = Fernet(key).decrypt(session_read.read())

                with open(file, "wb") as session_write:
                    session_write.write(decrypted)

                    return decrypted

        else:
            with open(file, "rb") as session_read:
                decrypted = Fernet(key).decrypt(session_read.read())

                return json.loads(decrypted.decode("utf-8"))

    # Get Application Version:
    def application_version(self):

        config = self.get_local_file("config.json")

        with open(config, "rb") as app_ver:
            version = json.loads(app_ver.read())
            return version["version"]

    # Get Latest Version:
    @staticmethod
    def latest_version():
        # Remote URL:
        repository_url = "https://api.github.com/repos/SelfTaught-HamzaCodes/Labelify/contents"

        # Retrieve data from URL:
        response = requests.get(repository_url)

        # Convert data to JSON:
        release_data = response.json()

        # Loop over all files:
        for file in release_data:

            # Check for the file which contains version and return:
            if file["name"] == "config.json":
                version_json = requests.get(file["download_url"])

                return version_json.json()["version"]

    # Check if update is available:
    def update_available(self):

        try:
            application = self.application_version()
            latest = self.latest_version()

            if application != latest:
                return "Update available"  # updates available.

            else:
                return "Update-to-date"  # No updates available.

        except Exception as e:
            return e

    # Set values for Excel file and Configurations:
    def set_excel_values(self, excel, sheet, row):

        self.excel_path = excel
        self.excel_sheet = sheet
        self.excel_row = row

    # Get values for Excel file and Configurations:
    def get_excel_values(self):

        return self.excel_path, self.excel_sheet, self.excel_row

    # Get Column Names:
    def get_column_names(self):

        # Generate Dataframe:
        excel_dataframe = pd.read_excel(self.excel_path, sheet_name=self.excel_sheet, header=int(self.excel_row) - 1)

        return list(excel_dataframe.columns)

    # Set path for Word file:
    def set_word_file(self, word_file):

        # Set File:
        self.word_path = word_file

        # Generate PlaceHolders:
        self.set_placeholders()

    # Get path for Word file:
    def get_word_file(self):

        return self.word_path

    # Set Placeholders:
    def set_placeholders(self):

        # Process Word File:
        processed = textract.process(self.word_path)
        processed = processed.decode("utf-8")

        # Extract Placeholders:
        expression = re.compile(r"{{(.*)}}")

        # Store Placeholders:
        self.placeholders = expression.findall(processed)

        # Sort Placeholders:
        self.placeholders.sort()

    # Extract Placeholders:
    def get_placeholders(self):

        return self.placeholders

    # Extract Fixed Values:
    def get_fixed_values(self, placeholder):

        # Get PATH for fixed.json:
        user_dir = os.path.join(os.environ['APPDATA'], "Label Generator")
        fixed = os.path.join(user_dir, "fixed.json")

        # Retrieve email:
        session_path = self.get_local_file("session.json")
        email = self.decrypt_file(session_path, self.generate_key(), retrieve=True)["email"]

        fixed_data = self.read_data(fixed)

        return fixed_data[email].get(placeholder, [])

    # Generate Label Document:
    def generate_label_doc(self, elements):

        # Open Excel File:
        packing_list = pd.read_excel(self.excel_path, sheet_name=self.excel_sheet, header=int(self.excel_row) - 1)

        # Open Label File:
        doc = DocxTemplate(self.word_path)

        # Create a combined document to store all labels
        final_doc = Document()

        # Get PATH for fixed.json:
        user_dir = os.path.join(os.environ['APPDATA'], "Label Generator")
        fixed = os.path.join(user_dir, "fixed.json")

        fixed_data = self.read_data(fixed)

        # Retrieve email:
        session_path = self.get_local_file("session.json")
        email = self.decrypt_file(session_path, self.generate_key(), retrieve=True)["email"]

        # Generate Labels:
        for i in range(len(packing_list)):

            context = {}

            for placeholder, element in elements.items():

                # Check Checkbox:

                # If not checked, means not-fixed value:
                if not element["checkbox_element"].value:

                    # If Dropdown had a value:
                    if element["dropdown_element"].value:
                        context[placeholder] = str(packing_list[element["dropdown_element"].value].iloc[i])
                        continue

                # If checked, means fixed value:
                else:

                    # If TextField had a value:
                    if element["text_field_element"].value:
                        context[placeholder] = element["text_field_element"].value

                        # Check if user wants value to be saved:
                        if element["save_checkbox"].value:

                            # If placeholder already exists:
                            if fixed_data[email].get(placeholder, 0):

                                # Check if value is already present:
                                if element["text_field_element"].value in fixed_data[email][placeholder]:
                                    continue

                                fixed_data[email][placeholder].append(element["text_field_element"].value)

                            else:
                                fixed_data[email][placeholder] = [element["text_field_element"].value]

                            self.write_data(fixed, fixed_data)

                        continue

                    elif element["dropdown_element"].value:
                        context[placeholder] = element["dropdown_element"].value
                        continue

                # Add Placeholder as the value, if not mentioned:
                context[placeholder] = placeholder

            # Render the document
            doc.render(context)

            # Save the rendered document to a temporary file
            temp_file = f'temp_rendered_doc_{i}.docx'
            doc.save(temp_file)

            # Open the temporary rendered document
            rendered_doc = Document(temp_file)

            # Extract the table from the rendered document
            rendered_table = rendered_doc.tables[0]  # Adjust the table index as needed

            # Create a new table in the final document
            final_table = final_doc.add_table(rows=len(rendered_table.rows), cols=len(rendered_table.columns))

            # Get the XML element of the rendered table
            table_xml = rendered_table._tbl.xml

            # Create a new table element in the final document
            new_table = etree.fromstring(table_xml)

            # Append the new table element to the final table
            final_table._tbl.append(new_table)

            # Add a page break after each rendered document
            final_doc.add_page_break()

            # Remove the temporary rendered document file
            # Uncomment the line below if you want to remove the temporary files
            os.remove(temp_file)

        # Return this and save it at designated spot:
        return final_doc

    # Set Feedback:
    def set_feedback(self, rating, likes, dislikes, updates, feedback):

        session = self.get_local_file("session.json")

        # Try to decrypt:
        try:
            # Try to decrypt file, using the key:
            self.decrypt_file(session, self.generate_key())

        except Exception:
            pass

        try:
            email = str(self.read_data(session)["email"])

            self.supabase.table('Feedback').insert({
                "email": email,
                "rate": rating,
                "likes": ", ".join(likes),
                "dislikes": ", ".join(dislikes),
                "updates": ", ".join(updates),
                "feedback": feedback

            }).execute()

            # Update Recorded to True:
            json_file = self.read_data(session)

            json_file["feedback_recorded"] = 1

            self.write_data(session, json_file)

            # Encrypt data:
            self.encrypt_file(session, self.generate_key())

            # Generate new hash value:
            self.get_hash(update=True)

            return "200"

        except Exception as e:
            return e
