import json
from pathlib import Path


# This file stores the student records between program runs.
DATA_FILE = Path(__file__).with_name("students.json")


# ============================================================
# CLASS 1: STUDENT
# A class is a blueprint for creating objects.
# This class represents one student and their information.
# ============================================================

class Student:

    def __init__(self, student_id, name, age, gender, course):
        # A constructor initializes the attributes of an object.
        # self refers to the particular Student object being created.
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.course = course

    @staticmethod
    def is_valid_student_id(student_id):
        # A static method performs a task that does not require
        # access to a particular object or the class itself.
        # Here, it checks that an ID contains exactly four digits.
        #
        # FIX: isascii() was added because isdigit() alone also accepts
        # digits from other writing systems (for example Arabic-Indic or
        # full-width digits). Those look like 1234 but are different text,
        # so the same ID could be registered twice. isascii() allows only
        # the normal digits 0-9.
        return (
            isinstance(student_id, str)
            and len(student_id) == 4
            and student_id.isascii()
            and student_id.isdigit()
        )

    @staticmethod
    def is_valid_age(age_text):
        # Another static method: it only checks text and needs no object.
        # FIX: this check was repeated in two places and could crash on
        # characters such as the superscript "2", which isdigit() accepts
        # but int() cannot convert. isascii() prevents that crash.
        return (
            isinstance(age_text, str)
            and age_text.isascii()
            and age_text.isdigit()
            and 1 <= int(age_text) <= 120
        )

    @classmethod
    def from_input(cls, existing_ids=None):
        # A class method receives the class through cls.
        # We use it to collect information and create a Student object.
        # existing_ids lets us reject an ID that is already registered.

        if existing_ids is None:
            existing_ids = ()

        while True:
            student_id = input(
                "Enter the last 4 digits of the student ID: "
            ).strip()

            if not cls.is_valid_student_id(student_id):
                print("Invalid ID. Enter exactly four digits.")
                continue

            # Check the ID immediately, before asking for other details.
            if student_id in existing_ids:
                print("A student with this ID already exists. Try another ID.")
                continue

            break

        name = input("Enter student name: ").strip()

        while not name:
            print("Name cannot be empty.")
            name = input("Enter student name: ").strip()

        while True:
            age_text = input("Enter student age: ").strip()

            if cls.is_valid_age(age_text):
                age = int(age_text)
                break

            print("Enter a valid age between 1 and 120.")

        while True:
            print("1. Male")
            print("2. Female")

            choice = input("Choose gender: ").strip()

            if choice == "1":
                gender = "Male"
                break
            elif choice == "2":
                gender = "Female"
                break
            else:
                print("Please choose 1 or 2.")

        course = input("Enter course: ").strip()

        while not course:
            print("Course cannot be empty.")
            course = input("Enter course: ").strip()

        # cls(...) creates and returns a new Student object.
        return cls(student_id, name, age, gender, course)

    def display_info(self):
        # This is an instance method because it uses self.
        # It displays the information belonging to this student.

        print("-" * 40)
        print(f"Student ID: {self.student_id}")
        print(f"Name:       {self.name}")
        print(f"Age:        {self.age}")
        print(f"Gender:     {self.gender}")
        print(f"Course:     {self.course}")
        print("-" * 40)

    def to_dict(self):
        # JSON cannot directly save a custom Student object.
        # This method converts the object into a dictionary.

        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "course": self.course
        }


# ============================================================
# CLASS 2: STUDENT MANAGER
# This class manages the collection of Student objects.
# ============================================================

class StudentManager:

    def __init__(self):
        # The dictionary stores Student objects.
        # Each four-digit student ID is a unique dictionary key.
        self.students = {}

        # Load previously saved records when the manager is created.
        self.load_records()

    def add_student(self):
        # Collect information and create a new Student object.
        # Pass existing dictionary keys so duplicate IDs are rejected
        # immediately when the user enters the ID.
        student = Student.from_input(self.students.keys())

        # Keep this second check as an extra safeguard.
        if student.student_id in self.students:
            print("A student with this ID already exists.")
            return

        # Store the object using its ID as the dictionary key.
        self.students[student.student_id] = student

        print("Student registered successfully!")

    def display_all(self):
        # Display all Student objects stored in the dictionary.

        if not self.students:
            print("No student records found.")
            return

        print("\n========== ALL STUDENTS ==========")

        # values() gives us the Student objects stored in the dictionary.
        for student in self.students.values():
            student.display_info()

    def search_by_id(self):
        # Find a student using their four-digit ID.

        student_id = input(
            "Enter the four-digit student ID: "
        ).strip()

        if not Student.is_valid_student_id(student_id):
            print("Invalid ID. Enter exactly four digits.")
            return

        # get() returns the matching object or None if it is missing.
        student = self.students.get(student_id)

        if student is not None:
            student.display_info()
        else:
            print("Student not found.")

    def search_by_name(self):
        # Search by full name or part of a name.
        # lower() makes the search ignore capitalization.

        search_name = input(
            "Enter the student name to search: "
        ).strip().lower()

        if not search_name:
            print("Please enter a name.")
            return

        found = False

        for student in self.students.values():
            if search_name in student.name.lower():
                student.display_info()
                found = True

        if not found:
            print("No matching student found.")

    def update_student(self):
        # Find a student before changing their information.

        student_id = input(
            "Enter the four-digit student ID: "
        ).strip()

        if not Student.is_valid_student_id(student_id):
            print("Invalid ID. Enter exactly four digits.")
            return

        student = self.students.get(student_id)

        if student is None:
            print("Student not found.")
            return

        # Press Enter to keep the existing value.
        print("Press Enter to keep the current information.")

        new_name = input(f"Name [{student.name}]: ").strip()

        if new_name:
            student.name = new_name

        new_age = input(f"Age [{student.age}]: ").strip()

        if new_age:
            if Student.is_valid_age(new_age):
                student.age = int(new_age)
            else:
                print("Invalid age. The old age will be kept.")

        print("1. Male")
        print("2. Female")

        new_gender = input(
            f"Gender [{student.gender}]: "
        ).strip()

        if new_gender == "1":
            student.gender = "Male"
        elif new_gender == "2":
            student.gender = "Female"
        elif new_gender:
            print("Invalid choice. The old gender will be kept.")

        new_course = input(f"Course [{student.course}]: ").strip()

        if new_course:
            student.course = new_course

        print("Student information updated successfully!")

    def delete_student(self):
        # Remove a student only after confirming their ID and deletion.

        student_id = input(
            "Enter the four-digit student ID: "
        ).strip()

        if not Student.is_valid_student_id(student_id):
            print("Invalid ID. Enter exactly four digits.")
            return

        if student_id not in self.students:
            print("Student not found.")
            return

        confirmation = input(
            "Delete this student? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            # del removes the dictionary entry for this student.
            del self.students[student_id]
            print("Student record deleted.")
        else:
            print("Deletion cancelled.")

    def course_statistics(self):
        # Count the number of students registered for each course.

        if not self.students:
            print("No student records available.")
            return

        course_counts = {}

        for student in self.students.values():
            # Standardize capitalization for counting.
            course_name = student.course.strip().casefold()

            if course_name in course_counts:
                course_counts[course_name] += 1
            else:
                course_counts[course_name] = 1

        print("\n========== COURSE STATISTICS ==========")

        for course, count in sorted(course_counts.items()):
            # title() makes the displayed course name easier to read.
            print(f"{course.title()}: {count} student(s)")

        print(f"Total students: {len(self.students)}")

    def save_records(self):
        # Convert Student objects to dictionaries before saving them.
        records = []

        for student in self.students.values():
            records.append(student.to_dict())

        try:
            # "w" opens the file for writing.
            # json.dump() writes the list to the JSON file.
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)

            print("Student records saved successfully.")

        except OSError:
            print("Error: Could not save student records.")

    def load_records(self):
        # Restore saved records when the program starts.

        if not DATA_FILE.exists():
            # The file will be created when records are first saved.
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                records = json.load(file)

        except (OSError, json.JSONDecodeError):
            # Handle a file that cannot be read or contains invalid JSON.
            print("Warning: Could not read the student data file.")
            return

        # The saved information should be a list of records.
        if not isinstance(records, list):
            print("Warning: The saved data has an invalid format.")
            return

        for record in records:
            # Each record should be a dictionary.
            if not isinstance(record, dict):
                continue

            student_id = record.get("student_id")
            name = record.get("name")
            age = record.get("age")
            gender = record.get("gender")
            course = record.get("course")

            # Validate the saved ID before using it.
            if not Student.is_valid_student_id(student_id):
                continue

            # Skip incomplete or invalid student information.
            if not isinstance(name, str) or not name.strip():
                continue

            if type(age) is not int or not 1 <= age <= 120:
                continue

            if gender not in ("Male", "Female"):
                continue

            if not isinstance(course, str) or not course.strip():
                continue

            # Ignore duplicate IDs in the saved file.
            if student_id in self.students:
                continue

            # Re-create the Student object from the saved information.
            student = Student(
                student_id,
                name,
                age,
                gender,
                course
            )

            self.students[student_id] = student


# ============================================================
# FUNCTION: SHOW MENU
# A function is a reusable block of code that performs a task.
# ============================================================

def show_menu():
    # Display the available actions.

    print("\n========================================")
    print("   STUDENT RECORD MANAGEMENT SYSTEM")
    print("========================================")
    print("1. Register student")
    print("2. Display all students")
    print("3. Search student by ID")
    print("4. Update student information")
    print("5. Delete student record")
    print("6. Search student by name")
    print("7. View course statistics")
    print("8. Save records")
    print("9. Exit")
    print("========================================")


# ============================================================
# FUNCTION: MAIN
# This function controls the overall program.
# ============================================================

def main():
    # Create a StudentManager object to manage the records.
    manager = StudentManager()

    # FIX: if the input stream ends (Ctrl+D / Ctrl+Z) or the user presses
    # Ctrl+C, Python raises EOFError or KeyboardInterrupt. Without this
    # try/except the program would crash with a long error message.
    try:
        run_menu(manager)
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Saving records before exit.")
        manager.save_records()


def run_menu(manager):
    # Keep displaying the menu until the user chooses to exit.
    while True:
        show_menu()

        choice = input("Choose an option (1-9): ").strip()

        # Call the appropriate method for the selected option.
        if choice == "1":
            manager.add_student()

        elif choice == "2":
            manager.display_all()

        elif choice == "3":
            manager.search_by_id()

        elif choice == "4":
            manager.update_student()

        elif choice == "5":
            manager.delete_student()

        elif choice == "6":
            manager.search_by_name()

        elif choice == "7":
            manager.course_statistics()

        elif choice == "8":
            manager.save_records()

        elif choice == "9":
            # Save the records before ending the program.
            manager.save_records()
            print("Thank you for using the system. Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


# This condition starts the program when main.py is run directly.
# It prevents main() from running automatically if this file is imported.
if __name__ == "__main__":
    main()
