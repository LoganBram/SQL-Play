import sqlite3


class EmployeeDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                dept_id INTEGER PRIMARY KEY,
                dept_name TEXT NOT NULL
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                emp_id INTEGER PRIMARY KEY,
                emp_name TEXT NOT NULL,
                emp_salary REAL NOT NULL,
                dept_id INTEGER NOT NULL,
                FOREIGN KEY (dept_id) REFERENCES Departments (dept_id)
            );
        ''')

        self.conn.commit()

    def add_department(self, dept_name):
        sql = "INSERT INTO Departments (dept_name) VALUES (?);"
        self.cursor.execute(sql, (dept_name,))
        self.conn.commit()

    def add_employee(self, emp_name, emp_salary, dept_id):
        sql = "INSERT INTO Employees (emp_name, emp_salary, dept_id) VALUES (?, ?, ?);"
        self.cursor.execute(sql, (emp_name, emp_salary, dept_id))
        self.conn.commit()

    def get_employee(self, emp_id):
        sql = "SELECT * FROM Employees WHERE emp_id=?;"
        self.cursor.execute(sql, (emp_id,))
        return self.cursor.fetchone()

    def get_employees_by_department(self, dept_id):
        sql = "SELECT * FROM Employees WHERE dept_id=?;"
        self.cursor.execute(sql, (dept_id,))
        return self.cursor.fetchall()

    def get_average_salary(self):
        sql = "SELECT AVG(emp_salary) FROM Employees;"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def update_salary(self, emp_id, new_salary):
        sql = "UPDATE Employees SET emp_salary=? WHERE emp_id=?;"
        self.cursor.execute(sql, (new_salary, emp_id))
        self.conn.commit()

    def delete_employee(self, emp_id):
        sql = "DELETE FROM Employees WHERE emp_id=?;"
        self.cursor.execute(sql, (emp_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    with EmployeeDB('employee.db') as db:
        db.add_department('Sales')
        db.add_department('Marketing')
        db.add_department('Engineering')

        db.add_employee('John Doe', 50000.00, 1)
        db.add_employee('Jane Smith', 60000.00, 2)
        db.add_employee('Bob Johnson', 70000.00, 3)
        db.add_employee('Alice Lee', 55000.00, 1)

        emp = db.get_employee(2)
        print(emp)

        employees = db.get_employees_by_department(1)
        print(employees)

        avg_salary = db.get_average_salary()
        print(f"Average salary: ${avg_salary:.2f}")

        db.update_salary(4, 60000.00)

        db.delete_employee(3)

        # display

        employees = db.get_employees_by_department(1)
        for emp in employees:
            print(emp)
