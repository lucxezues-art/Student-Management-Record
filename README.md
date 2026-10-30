# Student Record Management System

A command-line program written in Python that registers, searches, updates and deletes student records. It was built for the **PROG211 Object-Oriented Programming 1** individual assignment (*Real-World Solutions under DPG Standards*, Education domain) at Limkokwing University of Creative Technology, Sierra Leone.

> **Privacy notice:** this repository contains no real student information. All examples use fictional data. The data file (`students.json`) is created on your own computer and is excluded from Git by `.gitignore`.

## The problem it solves

Small schools and training centres often keep student lists on paper or in loose spreadsheets, which leads to duplicated IDs, typing mistakes and lost records. This program gives a simple, offline way to keep a clean register: every student has a unique four-digit ID, inputs are validated, and records are saved to a file between sessions.

## Features

| Menu option | What it does |
|---|---|
| 1. Register student | Adds a student; rejects invalid or duplicate IDs immediately |
| 2. Display all students | Lists every record |
| 3. Search by ID | Finds one student using the four-digit ID |
| 4. Update student | Changes name, age, gender or course (press Enter to keep a value) |
| 5. Delete student | Removes a record after a yes/no confirmation |
| 6. Search by name | Partial, case-insensitive name search |
| 7. Course statistics | Counts students per course (`Computing` and `computing` are counted together) |
| 8. Save records | Writes all records to `students.json` |
| 9. Exit | Saves and quits |

Records are also loaded automatically from `students.json` when the program starts.

## Object-oriented design

| Concept | Where it appears in `main.py` |
|---|---|
| Class 1: `Student` | Represents one student (attributes: `student_id`, `name`, `age`, `gender`, `course`) |
| Class 2: `StudentManager` | Manages the collection of `Student` objects and all menu actions |
| Objects and interaction | `StudentManager` creates `Student` objects and calls their methods (`display_info`, `to_dict`) |
| Instance methods | `display_info()`, `to_dict()`, and all `StudentManager` methods |
| Class method (`@classmethod`) | `Student.from_input()` collects input and builds a `Student` |
| Static methods (`@staticmethod`) | `Student.is_valid_student_id()` and `Student.is_valid_age()` |
| Data structure | A **dictionary** (`StudentManager.students`) stores every `Student` object, with the four-digit ID as the key, so duplicate IDs are impossible |

## Requirements

- Python 3.8 or newer (no extra packages needed; only the standard library is used)

## How to run (Windows PowerShell)

```powershell
git clone https://github.com/lucxezues-art/Student-Management-Record.git
cd Student-Management-Record
python main.py
```

If `python` is not recognised, try `py main.py`.

## Example usage

The following is an excerpt from a real run of the program using fictional data. Lines after each prompt are what the user typed. The menu is shown again between actions; it is omitted here for length.

```text
Choose an option (1-9): 1
Enter the last 4 digits of the student ID: 1001
Enter student name: Student One
Enter student age: 20
1. Male
2. Female
Choose gender: 2
Enter course: Computer Science
Student registered successfully!

Choose an option (1-9): 1
Enter the last 4 digits of the student ID: 1001
A student with this ID already exists. Try another ID.
Enter the last 4 digits of the student ID: 1003
...

Choose an option (1-9): 7

========== COURSE STATISTICS ==========
Computer Science: 2 student(s)
Statistics: 1 student(s)
Total students: 3

Choose an option (1-9): 5
Enter the four-digit student ID: 1002
Delete this student? (yes/no): yes
Student record deleted.
```

Saved file format (`students.json`):

```json
[
    {
        "student_id": "1001",
        "name": "Student One",
        "age": 20,
        "gender": "Female",
        "course": "Computer Science"
    }
]
```

## Input validation

- **Student ID:** exactly four characters, digits `0-9` only (leading zeros such as `0007` are kept). Letters, spaces, symbols and digits from other writing systems are rejected.
- **Age:** a whole number from 1 to 120.
- **Name and course:** cannot be empty.
- **Duplicate IDs:** checked as soon as the ID is typed, again before storing, and again when loading a saved file.
- **Saved file:** invalid, incomplete or duplicate records in `students.json` are skipped, and a corrupt file produces a warning instead of a crash.

## Digital Public Goods (DPG) considerations

| DPG principle | How this project addresses it |
|---|---|
| **Open source** | The complete source code is published in this public GitHub repository. |
| **Inclusive and accessible design** | Plain-text menus with numbered options, clear prompts and clear error messages. It runs offline with no account, internet connection or paid software, and uses plain text only, which assistive tools generally handle better than graphical interfaces (not yet tested with a screen reader). *Limitation:* the interface is English only. |
| **Privacy-respecting** | The program asks for no contact details, addresses, national IDs, grades or photos. Only a four-digit ID, name, age, gender and course are stored. Data stays on the user's own computer, is never sent anywhere, and `students.json` is excluded from Git. Real student data should not be committed to GitHub. |
| **Modular and reusable** | Responsibilities are separated: `Student` holds one student's data and validation, `StudentManager` handles the collection, and the menu code is in separate functions. The classes can be reused or imported into other programs. |

## Project files

```text
Student-Management-Record/
├── main.py        # Student, StudentManager, menu and program entry point
├── README.md      # This file
├── .gitignore     # Keeps students.json (local data) out of Git
└── students.json  # Created when you save records (not stored in the repository)
```

## Known limitations

- Records are written to disk when you choose option 8 or exit normally. Closing the window abruptly can lose unsaved changes.
- Data is stored as plain, unencrypted JSON.
- The gender field offers only two options.
- Command-line only; there is no graphical interface.

## Author

Individual assignment submission for PROG211, Limkokwing University of Creative Technology, Sierra Leone.
Author: *[your full name and student number]*
