import tkinter as tk
from tkinter import messagebox, ttk
import backend

class EmployeeApp:
    def __init__(self,master):
        self.master = master
        master.title("Employee Management App")

        master.configure(bg="lightblue")

        self.employee_id_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.department_var = tk.StringVar()

        #input field
        ttk.Label(master, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.employee_id_entry = ttk.Entry(master, textvariable=self.employee_id_var, state="disabled") #disabled fro new entry
        self.employee_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


        ttk.Label(master, text="First Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.first_name_entry = ttk.Entry(master, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(master, text="Last Name:").grid(row=2, column=0, padx=5,pady=5, sticky="w")
        self.last_name_entry = ttk.Entry(master, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


        ttk.Label(master, text="Department:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.department_entry = ttk.Entry(master, textvariable=self.department_var)
        self.department_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        #-----buttons-------
        self.insert_button = ttk.Button(master, text="Insert", command=self.insert_employee)
        self.insert_button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.view_button = ttk.Button(master, text="View", command=self.view_employee)
        self.view_button.grid(row=4, column=1, padx=5,pady=10, sticky="ew")

        self.update_button = ttk.Button(master, text="Update", command=self.update_employee)
        self.update_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        self.delete_button = ttk.Button(master, text="Delete", command=self.delete_employee)
        self.delete_button.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

        self.show_all_button = ttk.Button(master,text="Show All", command=self.show_all_employees)
        self.show_all_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")


        #====Display Area=====
        self.tree = ttk.Treeview(master, columns=("ID", "First Name", "Last Name", "Department"), show="headings")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Department", text="Department")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(7, weight = 1)
        self.tree.bind("<ButtonRelease-1>", self.populate_fields) #select item to populate the fields
        self.populate_employee_list() # Initial population of the list


    def clear_fields(self):
        #clears the input fields
        self.employee_id_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.department_var.set("")
        self.employee_id_entry.config(state = "disabled")

    def populate_fields(self, event):
        #populate the input fields with the selected employee's data
        selected_item = self.tree.selection()
        if selected_item:
            employee_id, first_name, last_name, department = self.tree.item(selected_item[0], "values")
            self.employee_id_var.set(employee_id)
            self.first_name_var.set(first_name)
            self.last_name_var.set(last_name)
            self.department_var.set(department)
            self.employee_id_entry.config(state = "normal") #enable the id field for updates/ deletes
        else:
            self.clear_fields()
            self.employee_id_entry.config(state = "disabled")


    def populate_employee_list(self):
        #fetches all the employees and displays them in the tree view
        employees = backend.fetch_all_employees()
        if employees:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for employee in employees:
                self.tree.insert("", tk.END, values=employee)

    def insert_employee(self):
        #inserts a new employee into the database
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        department = self.department_var.get()

        if first_name and last_name and department:
            if backend.insert_employee(first_name, last_name, department):
                messagebox.showinfo("Success","Employee inserted successfully!")
                self.populate_employee_list()
                self.clear_fields()
            else:
                messagebox.showerror("Error","Failed to insert employee.")
        else:
            messagebox.showerror("Error","Please fill in all the fields.")

    def view_employee(self):
        #views the details of the employee by ID
        employee_id = self.employee_id_var.get()
        if employee_id:
            employee = backend.fetch_employee(employee_id)
            if employee:
                messagebox.showinfo("Employee Details",f"ID: {employee[0]}\nFirst Name: {employee[1]}\nLast Name: {employee[2]}\nDepartment: {employee[3]}")
            else:
                messagebox.showerror("Error", f"Employee with ID {employee_id} not found.")
        else:
            messagebox.showerror("Error", "Please enter an employee ID to view.")


    def update_employee(self):
        #updates an existing employee data
        employee_id = self.employee_id_var.get()
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        department = self.department_var.get()

        if employee_id and first_name and last_name and department:
            if backend.update_employee(employee_id, first_name, last_name, department):
                messagebox.showinfo("Success", "Employee updated successfully!")
                self.populate_fields("event")
            else:
                messagebox.showerror("Error",f"Failed to update employee with ID {employee_id}")
        else:
            messagebox.showerror("Error","Please select an employee to update and fill in all fields.")


    def delete_employee(self):
        #delate an employee from the database
        employee_id = self.employee_id_var.get()
        if employee_id:
            if messagebox.askyesno("Confirm",f"Are you sure you want to delete the employee with employee ID {employee_id}?"):
                if backend.delete_employee(employee_id):
                    messagebox.showinfo("Success", "Employee deleted successfully!")
                    self.populate_employee_list()
                    self.clear_fields()
                else:
                    messagebox.showerror("Error",f"Failed to delate employee with employee ID {employee_id}.")
        else:
            messagebox.showerror("Error","Please select an employee to delete")


    def show_all_employees(self):
        #refreshes the employee list to show all the entries 
        self.populate_employee_list()

if __name__ == "__main__":
    print("Running gui_frontend.py")
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()


