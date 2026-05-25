import os
import json
from datetime import datetime

class Student:
    """Class to represent a student with marks and attendance"""
    
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.marks = {}  # Dictionary to store marks: {subject: score}
        self.attendance = set()  # Set to store attendance dates
    
    def add_marks(self, subject, score):
        """Add marks for a subject"""
        if not isinstance(score, (int, float)):
            raise ValueError("Marks must be a number")
        if score < 0 or score > 100:
            raise ValueError("Marks must be between 0 and 100")
        self.marks[subject] = score
    
    def get_average(self):
        """Calculate average marks"""
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)
    
    def mark_attendance(self, date=None):
        """Mark attendance for a date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        self.attendance.add(date)
    
    def get_attendance_percentage(self, total_days):
        """Calculate attendance percentage"""
        if total_days == 0:
            return 0
        return (len(self.attendance) / total_days) * 100
    
    def to_dict(self):
        """Convert student data to dictionary for saving"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "marks": self.marks,
            "attendance": list(self.attendance)
        }
    
    @staticmethod
    def from_dict(data):
        """Create student from dictionary"""
        student = Student(data["student_id"], data["name"])
        student.marks = data["marks"]
        student.attendance = set(data["attendance"])
        return student
    
    def __str__(self):
        return f"ID: {self.student_id} | Name: {self.name} | Avg: {self.get_average():.2f}"


class StudentManagementSystem:
    """Main system to manage students"""
    
    def __init__(self, filename="students_data.json"):
        self.students = {}
        self.filename = filename
        self.load_data()
    
    def add_student(self, student_id, name):
        """Add a new student"""
        if student_id in self.students:
            raise ValueError(f"Student with ID {student_id} already exists")
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        
        self.students[student_id] = Student(student_id, name)
        print(f"✓ Student '{name}' added successfully!")
    
    def remove_student(self, student_id):
        """Remove a student"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        
        name = self.students[student_id].name
        del self.students[student_id]
        print(f"✓ Student '{name}' removed successfully!")
    
    def add_marks(self, student_id, subject, score):
        """Add marks for a student"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        
        self.students[student_id].add_marks(subject, score)
        print(f"✓ Marks added for {self.students[student_id].name} in {subject}")
    
    def mark_attendance(self, student_id, date=None):
        """Mark attendance for a student"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        
        self.students[student_id].mark_attendance(date)
        print(f"✓ Attendance marked for {self.students[student_id].name}")

    def edit_student_name(self, student_id, new_name):
        """Edit a student's name"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        if not new_name or not isinstance(new_name, str):
            raise ValueError("Name must be a non-empty string")
        old_name = self.students[student_id].name
        self.students[student_id].name = new_name
        print(f"✓ Name updated from '{old_name}' to '{new_name}'")

    def edit_student_id(self, old_id, new_id):
        """Edit a student's ID"""
        if old_id not in self.students:
            raise ValueError(f"Student with ID {old_id} not found")
        if new_id in self.students:
            raise ValueError(f"Student with ID {new_id} already exists")
        student = self.students.pop(old_id)
        student.student_id = new_id
        self.students[new_id] = student
        print(f"✓ Student ID updated from '{old_id}' to '{new_id}'")

    def edit_student_marks(self, student_id, subject, new_score):
        """Edit marks for a specific subject"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        student = self.students[student_id]
        if subject not in student.marks:
            raise ValueError(f"Subject '{subject}' not found. Use 'Add Marks' to add a new subject.")
        student.add_marks(subject, new_score)
        print(f"✓ Marks for '{subject}' updated to {new_score} for {student.name}")

    def edit_student_attendance(self, student_id, action, date):
        """Edit attendance by adding or removing a specific date"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        student = self.students[student_id]
        if action == 'A':
            student.attendance.add(date)
            print(f"✓ Date '{date}' added to attendance for {student.name}")
        elif action == 'R':
            if date in student.attendance:
                student.attendance.remove(date)
                print(f"✓ Date '{date}' removed from attendance for {student.name}")
            else:
                print(f"✗ Date '{date}' not found in attendance records")
        else:
            raise ValueError("Action must be 'A' (Add) or 'R' (Remove)")

    def display_student(self, student_id):
        """Display detailed information about a student"""
        if student_id not in self.students:
            raise ValueError(f"Student with ID {student_id} not found")
        
        student = self.students[student_id]
        print(f"\n{'='*50}")
        print(f"Student ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Marks: {student.marks if student.marks else 'No marks recorded'}")
        print(f"Average: {student.get_average():.2f}")
        print(f"Attendance Days: {len(student.attendance)}")
        print(f"Attendance Dates: {sorted(student.attendance) if student.attendance else 'None'}")
        print(f"{'='*50}\n")
    
    def display_all_students(self):
        """Display all students"""
        if not self.students:
            print("No students in the system")
            return
        
        print(f"\n{'='*50}")
        print(f"Total Students: {len(self.students)}")
        print(f"{'='*50}")
        for student in self.students.values():
            print(student)
        print(f"{'='*50}\n")
    
    def save_data(self):
        """Save all student data to JSON file"""
        try:
            data = {
                student_id: student.to_dict()
                for student_id, student in self.students.items()
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"✓ Data saved to {self.filename}")
        except IOError as e:
            print(f"✗ Error saving data: {e}")
    
    def load_data(self):
        """Load student data from JSON file"""
        if not os.path.exists(self.filename):
            print(f"No existing data file found. Starting fresh.")
            return
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            self.students = {
                student_id: Student.from_dict(student_data)
                for student_id, student_data in data.items()
            }
            print(f"✓ Data loaded from {self.filename}")
        except IOError as e:
            print(f"✗ Error loading data: {e}")
    
    def get_top_students(self, n=5):
        """Get top N students by average"""
        if not self.students:
            print("No students to display")
            return
        
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.get_average(),
            reverse=True
        )[:n]
        
        print(f"\n{'='*50}")
        print(f"Top {n} Students by Average")
        print(f"{'='*50}")
        for i, student in enumerate(sorted_students, 1):
            print(f"{i}. {student.name} - Average: {student.get_average():.2f}")
        print(f"{'='*50}\n")


def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("SMART STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Add Marks")
    print("4. Mark Attendance")
    print("5. View Student Details")
    print("6. View All Students")
    print("7. View Top Students")
    print("8. Save Data")
    print("9. Edit Student Name")
    print("10. Edit Student ID")
    print("11. Edit Student Marks")
    print("12. Edit Student Attendance")
    print("13. Exit")
    print("="*50)


def main():
    """Main function to run the system"""
    system = StudentManagementSystem()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-13): ").strip()
        
        try:
            if choice == '1':
                student_id = input("Enter Student ID: ").strip()
                name = input("Enter Student Name: ").strip()
                system.add_student(student_id, name)
            
            elif choice == '2':
                student_id = input("Enter Student ID to remove: ").strip()
                system.remove_student(student_id)
            
            elif choice == '3':
                student_id = input("Enter Student ID: ").strip()
                subject = input("Enter Subject: ").strip()
                try:
                    score = float(input("Enter Marks (0-100): "))
                    system.add_marks(student_id, subject, score)
                except ValueError:
                    print("✗ Please enter a valid number for marks")
            
            elif choice == '4':
                student_id = input("Enter Student ID: ").strip()
                date_input = input("Enter Date (YYYY-MM-DD) or press Enter for today: ").strip()
                date = date_input if date_input else None
                system.mark_attendance(student_id, date)
            
            elif choice == '5':
                student_id = input("Enter Student ID: ").strip()
                system.display_student(student_id)
            
            elif choice == '6':
                system.display_all_students()
            
            elif choice == '7':
                try:
                    n = int(input("How many top students to display? "))
                    system.get_top_students(n)
                except ValueError:
                    print("✗ Please enter a valid number")
            
            elif choice == '8':
                system.save_data()

            elif choice == '9':
                student_id = input("Enter Student ID: ").strip()
                new_name = input("Enter new name: ").strip()
                system.edit_student_name(student_id, new_name)

            elif choice == '10':
                old_id = input("Enter current Student ID: ").strip()
                new_id = input("Enter new Student ID: ").strip()
                system.edit_student_id(old_id, new_id)

            elif choice == '11':
                student_id = input("Enter Student ID: ").strip()
                subject = input("Enter subject to edit: ").strip()
                try:
                    new_score = float(input("Enter new marks (0-100): "))
                    system.edit_student_marks(student_id, subject, new_score)
                except ValueError:
                    print("✗ Please enter a valid number for marks")

            elif choice == '12':
                student_id = input("Enter Student ID: ").strip()
                if student_id in system.students:
                    current = sorted(system.students[student_id].attendance)
                    print(f"Current attendance dates: {current if current else 'None'}")
                action = input("(A)dd or (R)emove a date? ").strip().upper()
                date = input("Enter Date (YYYY-MM-DD): ").strip()
                system.edit_student_attendance(student_id, action, date)

            elif choice == '13':
                save_choice = input("Save data before exiting? (y/n): ").strip().lower()
                if save_choice == 'y':
                    system.save_data()
                print("✓ Goodbye!")
                break
            
            else:
                print("✗ Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()