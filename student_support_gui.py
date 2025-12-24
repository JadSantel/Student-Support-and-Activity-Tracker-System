import customtkinter as ctk
from tkinter import messagebox

class User:
    def __init__(self, name, age, role):
        self.name = name
        self.age = age 
        self.role = role
        self.points = 0

    def add_points(self, activity):
        match activity:
            case "study":
                self.points += 3
                print("Study session logged (+3 points)")
            case "exercise":
                self.points += 2
                print("Exercise logged (+2 points)")
            case "project":
                self.points += 4
                print("Project work logged (+4 points)")
            case "idle":
                self.points -= 1
                print("Idle time logged (-1 point)")
            case _:
                print("Invalid Activity!")
            
    def get_status(self):
        if self.points > 20:
            return "Excellent"
        elif self.points > 10:
            return "Good"
        elif self.points > 0:
            return "Needs Improvement"
        else:
            return "At Risk"

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Role: {self.role}")
        print(f"Points: {self.points}")
        print(f"Status: {self.get_status()}")

def show_menu():
    print("===== Student Support & Activity Tracker =====")
    print("1. Register User")
    print("2. Log Activity")
    print("3. View User Summary")
    print("4. Evaluate Status")
    print("5. Exit")

def get_int_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("Please enter a valid number.")

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        else:
            print("Input cannot be empty.")

def get_valid_role(prompt):
    while True:
        role = input(prompt).strip().lower()

        if role == "student" or role == "staff":
            return role.capitalize()
        else:
            print("Invalid role. Please enter 'Student' or 'Staff'.")

def get_valid_activity(prompt):
    valid_activities = {"study, exercise, project, idle"}

    while True:
        activity = input(prompt).lower().strip()

        if activity in valid_activities:
            return activity
        else:
            print("Invalid activity. Please try again.")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Student Support & Activity Tracker")
app.geometry("500x400")

#Button for submission of new user
def submit_user():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    role = role_combo.get()

    if not name:
        messagebox.showerror("Input Error","Name cannot be empty.")
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Input Error","Invalid age.")
        return
    
    user = User(name, int(age), role)
    users.append(user)

    messagebox.showinfo("Success",f"User {name} registered successfully.")

    name_entry.delete(0, "end")
    age_entry.delete(0, "end")
    role_combo.set("Student")

    refresh_user_list()

#Refreshing User List for Logged Users
def refresh_user_list():
    if users:
        user_combo.configure(values=[user.name for user in users])
        user_combo.set(users[0].name)
    else:
        user_combo.configure(values=[])
        user_combo.set("")

#Logging Activity
def open_activity():
    refresh_user_list()
    activity_frame.pack(pady=20, fill="both", expand=True)

def refresh_summary():

    for widget in summary_container.winfo_children():
        widget.destroy()
    
    if not users:
        ctk.CTkLabel(summary_container,text="No registered users.").pack(pady=10)
        return
    
    for user in users:
        user_card = ctk.CTkFrame(summary_container)
        user_card.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(user_card,text=f"Name: {user.name}").pack(anchor="w",padx=10)

        ctk.CTkLabel(user_card,text=f"Role: {user.role}").pack(anchor="w",padx=10)

        ctk.CTkLabel(user_card,text=f"Points: {user.points}").pack(anchor="w",padx=10)

        ctk.CTkLabel(user_card,text=f"Status: {user.get_status()}").pack(anchor="w",padx=10)

#Function for viewing summary
def open_summary():
    refresh_summary()
    summary_frame.pack(pady=20, fill="both", expand=True)

def open_register():
    register_frame.pack(pady=20, fill="both", expand=True)

#Function for logging activities
def submit_activity():
    selected_name = user_combo.get()
    selected_activity = activity_combo.get().lower()

    if not selected_name:
        messagebox.showerror("Error","Invalid user")
        return
    
    for user in users:
        if user.name == selected_name:
            user.add_points(selected_activity)
            messagebox.showinfo("Success", f"{selected_activity} logged for {user.name}")
        return

users = []

#Frame for user registration 
register_frame = ctk.CTkFrame(app)

ctk.CTkLabel(register_frame, text="Register User", font=("Arial",18)).pack(pady=10)

submit_btn = ctk.CTkButton(register_frame,text="Submit", command=submit_user)
submit_btn.pack(pady=10)

name_entry = ctk.CTkEntry(register_frame, placeholder_text="Enter Name")
name_entry.pack(pady=5)

age_entry = ctk.CTkEntry(register_frame, placeholder_text="Enter Age")
age_entry.pack(pady=5)

role_combo = ctk.CTkComboBox(register_frame, values=["Student","Staff"])
role_combo.pack(pady=5)

btn_register = ctk.CTkButton(app, text="Register User", command=open_register)
btn_register.pack(pady=10)

btn_activity = ctk.CTkButton(app, text="Log Activity", command=open_activity)
btn_activity.pack(pady=10)

btn_summary = ctk.CTkButton(app, text="View Summary", command=open_summary)
btn_summary.pack(pady=10)

#Frame for logging activity
activity_frame = ctk.CTkFrame(app)

ctk.CTkLabel(activity_frame, text="Log Activity", font=("Arial",18)).pack(pady=10)

user_combo = ctk.CTkComboBox(activity_frame, values=[])
user_combo.pack(pady=5)

activity_combo = ctk.CTkComboBox(activity_frame,values=["Study", "Exercise", "Project", "Idle"])

activity_combo.set("Study")
activity_combo.pack(pady=5)

log_btn = ctk.CTkButton(activity_frame, text="Log Activity",command=submit_activity)
log_btn.pack(pady=10)

# Frame for Summary
summary_frame = ctk.CTkFrame(app)

ctk.CTkLabel(summary_frame, text="User Summary", font=("Arial",18)).pack(pady=10)

summary_container = ctk.CTkScrollableFrame(summary_frame, width=450, height=250)
summary_container.pack(pady=10, fill="both",expand=True)

app.mainloop()






