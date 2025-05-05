import mysql.connector

#database configuration 

mydata_Base_Configuration = {
    'host': 'localhost',
    'user': 'root',
    'password': '1986MANDAY',
    'database': 'company'
}

def connect_db():
    #connects to the mysql database.
    try:
        mydb = mysql.connector.connect(**mydata_Base_Configuration)
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None
    

def close_db(mydb):
    #close the database connection
    if mydb and mydb.is_connected():
        mydb.close()
        print("Database connection closed successfully!")


def insert_employee(first_name, last_name, department):
    #inserts a new employee into the database
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "INSERT INTO employeess (first_name, last_name, department) VALUES(%s, %s,%s)"
            val = (first_name, last_name, department)
            cursor.execute(sql, val)
            mydb.commit()
            print(f"{cursor.rowcount} record is inserted.")
            close_db(mydb)
            return True
        except mysql.connector.Error as err:
            print(f"An error {err} occurred while inserting the employee data.")
            mydb.rollback()
            close_db(mydb)
            return False
    return False

def fetch_employee(employee_id):
    #fetching a single employee details or record by ID
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "SELECT employee_id, first_name, last_name, department FROM employeess WHERE employee_id = %s"
            val = (employee_id,)
            cursor.execute(sql, val)
            results = cursor.fetchone()
            close_db(mydb)
            return results
        except mysql.connector.Error as err:
            print(f"Erro fetching employee: {err}")
            close_db(mydb)
            return None
    return None


def fetch_all_employees():
    #fetch all the employee records form the database
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "SELECT employee_id, first_name, last_name, department FROM employeess"
            cursor.execute(sql)
            results = cursor.fetchall()
            close_db(mydb)
            return results
        except mysql.connector.Error as err:
            print(f"Error fetching all Employee: {err}")
            close_db(mydb)
            return None
    return None



def update_employee(employee_id, first_name, last_name, department):
    #update ann existing employee record
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
            # Check if the employee_id exists
            check_sql = "SELECT COUNT(*) FROM employeess WHERE employee_id = %s"
            cursor.execute(check_sql, (employee_id,))
            result = cursor.fetchone()
            if result[0] == 0:
                print(f"Employee with ID {employee_id} does not exist.")
                close_db(mydb)
                return False
            else:
            #perform the update operation
                sql = "UPDATE employeess SET first_name=%s, last_name=%s, department = %s WHERE employee_id = %s"
                val = (first_name, last_name, department, employee_id)
                cursor.execute(sql, val)
                mydb.commit()
                print(f"{cursor.rowcount} record(s) updated!")
                close_db(mydb)
                return True
        except mysql.connector.Error as err:
            print(f"Error updating employee: {err}")
            mydb.rollback()
            close_db(mydb)
            return False
    return False



def delete_employee(employee_id):
    #delete an employee record by ID
    mydb = connect_db()
    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM employeess WHERE employee_id = %s"
            val = (employee_id,)
            cursor.execute(sql, val)
            mydb.commit()
            print(f"{cursor.rowcount} records deleted.")
            close_db(mydb)
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting employee: {err}")
            mydb.rollback()
            close_db(mydb)
            return False
    return False


def test_backend():
    #Example usage (for testing the backend functions)
    #Make sure your database and the table are set up first

    #create the table employees if table does note exist
    mybd_test = connect_db()
    if mybd_test:
        cursor_test = mybd_test.cursor()
        cursor_test.execute("""
        CREATE TABLE IF NOT EXISTS employeess (employee_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        department VARCHAR(50))
        """)
        close_db(mybd_test)

#insert a new employee
    insert_employee("Joan", "Doe","IT")

#Fetch all employees
    all_employees = fetch_all_employees()
    if all_employees:
        print("\nEmployee:")
        for employee in all_employees:
            print(employee)


#fetching the employee by Id
    employee = fetch_employee(1)
    if employee:
        print("\nEmployee with ID 1:")
        print(employee)

#update an employee
    update_employee(8, "Jonathan","Cane", "Commerce")
#Fetch all employees again to see the update
    all_employees_updated = fetch_all_employees()
    if all_employees_updated:
        print("\nALL employees after update:")
        for employee in all_employees_updated:
            print(employee)


#deleting an employee
    delete_employee(1)

#fetching all employees after deletion
    all_employee_deleted = fetch_all_employees()
    if all_employee_deleted:
        print("\nAll employees after deletion")
        for employee in all_employee_deleted:
            print(employee)


if __name__ == "__main__":
    print("Running backend.py")
    test_backend()




