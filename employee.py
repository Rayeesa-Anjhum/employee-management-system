import json
import os

# ================== CONSTANTS ==================

FILE_NAME = "employees.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

EMPLOYEE_NOT_FOUND = "Employee Not Found"
EMPLOYEE_EXISTS = "Employee ID already exists"
INVALID_SALARY = "Invalid Salary Input"
NO_RECORDS = "No Employee Records Found"


# ================== CUSTOM EXCEPTION ==================

class EmployeeNotFoundException(Exception):
    pass


class DuplicateEmployeeException(Exception):
    pass


# ================== EMPLOYEE MANAGER CLASS ==================

class EmployeeManager:

    def __init__(self):
        self.filename = FILE_NAME
        self.employees = self.load_data()

    # ---------- Load Data ----------
    def load_data(self):
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    # ---------- Save Data ----------
    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.employees, file, indent=4)

    # ---------- Add Employee ----------
    def add_employee(self):
        emp_id = input("Enter Employee ID: ").strip()

        if any(emp["id"] == emp_id for emp in self.employees):
            raise DuplicateEmployeeException(EMPLOYEE_EXISTS)

        name = input("Enter Name: ").strip()
        department = input("Enter Department: ").strip()

        try:
            salary = float(input("Enter Salary: "))
            if salary < 0:
                raise ValueError
        except ValueError:
            print(INVALID_SALARY)
            return

        employee = {
            "id": emp_id,
            "name": name,
            "department": department,
            "salary": salary
        }

        self.employees.append(employee)
        self.save_data()

        print("Employee Added Successfully ✅\n")

    # ---------- View Employees ----------
    def view_employees(self):
        if not self.employees:
            print(NO_RECORDS, "\n")
            return

        print("\n----- Employee List -----")
        for emp in self.employees:
            print(f"ID: {emp['id']}")
            print(f"Name: {emp['name']}")
            print(f"Department: {emp['department']}")
            print(f"Salary: {emp['salary']}")
            print("---------------------------")
        print()

    # ---------- Search ----------
    def search_employee(self):
        emp_id = input("Enter Employee ID to search: ").strip()

        for emp in self.employees:
            if emp["id"] == emp_id:
                print("Employee Found ✅")
                print(emp, "\n")
                return

        raise EmployeeNotFoundException(EMPLOYEE_NOT_FOUND)

    # ---------- Update ----------
    def update_employee(self):
        emp_id = input("Enter Employee ID to update: ").strip()

        for emp in self.employees:
            if emp["id"] == emp_id:
                emp["name"] = input("Enter New Name: ").strip()
                emp["department"] = input("Enter New Department: ").strip()

                try:
                    salary = float(input("Enter New Salary: "))
                    if salary < 0:
                        raise ValueError
                    emp["salary"] = salary
                except ValueError:
                    print(INVALID_SALARY)
                    return

                self.save_data()
                print("Employee Updated Successfully ✅\n")
                return

        raise EmployeeNotFoundException(EMPLOYEE_NOT_FOUND)

    # ---------- Delete ----------
    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ").strip()

        for emp in self.employees:
            if emp["id"] == emp_id:
                self.employees.remove(emp)
                self.save_data()
                print("Employee Deleted Successfully ✅\n")
                return

        raise EmployeeNotFoundException(EMPLOYEE_NOT_FOUND)

    # ---------- Report ----------
    def generate_report(self):
        if not self.employees:
            print(NO_RECORDS, "\n")
            return

        total_salary = sum(emp["salary"] for emp in self.employees)
        average_salary = total_salary / len(self.employees)

        print("\n----- Employee Report -----")
        print("Total Employees:", len(self.employees))
        print("Total Salary Expense:", total_salary)
        print("Average Salary:", round(average_salary, 2))
        print("----------------------------\n")


# ================== LOGIN SYSTEM ==================

def login():
    print("====== Employee Management Login ======")
    username = input("Username: ")
    password = input("Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login Successful ✅\n")
        return True
    else:
        print("Invalid Credentials ❌\n")
        return False


# ================== MAIN PROGRAM ==================

def main():
    if not login():
        return

    manager = EmployeeManager()

    while True:
        print("====== MENU ======")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("Enter Choice: ")

        try:
            if choice == "1":
                manager.add_employee()
            elif choice == "2":
                manager.view_employees()
            elif choice == "3":
                manager.search_employee()
            elif choice == "4":
                manager.update_employee()
            elif choice == "5":
                manager.delete_employee()
            elif choice == "6":
                manager.generate_report()
            elif choice == "7":
                print("Exiting Program 👋")
                break
            else:
                print("Invalid Choice ❗\n")

        except EmployeeNotFoundException as e:
            print(e, "\n")
        except DuplicateEmployeeException as e:
            print(e, "\n")


if __name__ == "__main__":
    main()
