import customtkinter as ctk
from tkinter import messagebox
import json
import os

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
app.geometry("600x500")

users = []

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
    refresh_summary()
    save_users_to_file()


#Refreshing User List for Logged Users
def refresh_user_list():
    names = [user.name for user in users]

    user_combo.configure(values=names)

    if names:
        user_combo.set(names[-1])
        log_btn.configure(state="normal")        
    else:
        user_combo.set("")
        log_btn.configure(state="disabled")
        

#Logging Activity
def open_activity():
    refresh_user_list()
    activity_frame.pack(pady=20, fill="both", expand=True)

#Deletes Users
def delete_user(user):
    confirm = messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete {user.name}?")

    if confirm:
        users.remove(user)
        messagebox.showinfo("Deleted",f"{user.name} has been removed.")
        refresh_user_list()
        refresh_summary()
        save_users_to_file()

#Edit logged user
def open_edit_user(user):
    hide_content_frames()
    edit_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for widget in edit_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(edit_frame, text=F"Editing {user.name}", font=("Arial", 18)).pack(pady=10)

    name_entry = ctk.CTkEntry(edit_frame, placeholder_text="Name")
    name_entry.insert(0, user.name)
    name_entry.pack(pady=5)

    age_entry = ctk.CTkEntry(edit_frame, placeholder_text="Age")
    age_entry.insert(0, user.age)
    age_entry.pack(pady=5)

    role_entry = ctk.CTkEntry(edit_frame, placeholder_text="Role")
    role_entry.insert(0, user.role)
    role_entry.pack(pady=5)

    def apply_changes():
        new_name = name_entry.get().strip()
        new_age = age_entry.get().strip()
        new_role = role_combo.get()

        if not new_name or not new_age.isdigit() or int(new_age) <= 0:
            messagebox.showerror("Invalid Input", "Please enter valid information.")
            return
        
        user.name = new_name
        user.age = new_age
        user.role = new_role

        messagebox.showinfo("Success", "User updated successfully!")
        refresh_user_list()
        refresh_summary()
        hide_content_frames()
        save_users_to_file()
    
    ctk.CTkButton(edit_frame, text="Save Changes", command=apply_changes).pack(pady=15)
    
#Updates the logged activities and users
def refresh_summary():
    for widget in summary_container.winfo_children():
        widget.destroy()
    
    if not users:
        ctk.CTkLabel(summary_container,text="No registered users.").pack(pady=10)
        return
    
    for user in users:
        user_card = ctk.CTkFrame(summary_container, fg_color="#62676D")
        user_card.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(user_card,text=f"Name: {user.name}").pack(anchor="w",padx=10)

        ctk.CTkLabel(user_card,text=f"Role: {user.role}").pack(anchor="w",padx=10)

        ctk.CTkLabel(user_card,text=f"Points: {user.points}").pack(anchor="w",padx=10)

        status = user.get_status()

        if status == "Excellent":
            color = "#34E710"
        elif status == "Good":
            color = "#32CD32"
        elif status == "Needs Improvement":
            color = "#FFD700"
        else:
            color = "#DC143C"
        
        ctk.CTkLabel(user_card, text=f"Status: {status}",
                     text_color=color
                     ).pack(anchor="w", padx=10)
        
        button_row = ctk.CTkFrame(user_card)
        button_row.pack(pady=5) 

        delete_btn = ctk.CTkButton(button_row,text="Delete User",
                                    fg_color="#B22222", hover_color="#8B0000",
                                    command=lambda u=user: delete_user(u))
        delete_btn.grid(row=0, column=0, padx=3)

        edit_btn = ctk.CTkButton(button_row,text="Edit User",
                                   fg_color="#1E90FF", hover_color="#1C86EE",
                                   command=lambda u=user: open_edit_user(u))
        edit_btn.grid(row=0, column=1, padx=3)

#Saving Users JSON
def save_users_to_file(filename="users.json"):
    data = []
    for user in users:
        data.append({
            "name": user.name,
            "age": user.age,
            "role": user.role,
            "points": user.points,
        })
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

#Load Users JSON
def load_users_from_files(filename="users.json"):
    if not os.path.exists(filename):
        return
    
    with open(filename, "r") as f:
        data = json.load(f)

    users.clear()
    for u in data:
        user = User(u["name"], u["age"], u["role"])
        user.points = u["points"]
        users.append(user)
    
    refresh_user_list()
    refresh_summary()


#Function for viewing summary
def open_summary():
    hide_content_frames()
    refresh_summary()
    summary_frame.pack(pady=20, fill="both", expand=True)

def open_register():
    hide_content_frames()
    register_frame.pack(pady=20, fill="both", expand=True)
    refresh_summary()

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
            refresh_summary()
            return
    
    save_users_to_file()
    messagebox.showerror("Internal Error","Selected user was not found.")

def hide_content_frames():
    register_frame.pack_forget()
    activity_frame.pack_forget()
    edit_frame.pack_forget()

def open_register():
    hide_content_frames()
    register_frame.pack(fill="both", expand= True)

def open_activity():
    hide_content_frames()
    refresh_user_list()
    activity_frame.pack(fill="both", expand=True)
    refresh_summary()

#Main Container Structure
main_container = ctk.CTkFrame(app)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

top_container = ctk.CTkFrame(main_container)
top_container.pack(fill="both", expand=True)

summary_frame = ctk.CTkFrame(main_container)
summary_frame.pack(fill="x", pady=10)

nav_frame = ctk.CTkFrame(top_container, width=180)
nav_frame.pack(side="left", fill="y", padx=(0,10))

content_frame = ctk.CTkFrame(top_container)
content_frame.pack(side="right", fill="both", expand=True)

edit_frame = ctk.CTkFrame(content_frame)

#Navigation frame buttons
ctk.CTkLabel(nav_frame, text="Menu",font=("Arial", 16)).pack(pady=15)
ctk.CTkButton(nav_frame, text="Register User",command=open_register).pack(fill="x", pady=5)
ctk.CTkButton(nav_frame, text="Log Activity",command=open_activity).pack(fill="x", pady=5)
ctk.CTkButton(nav_frame, 
              text="Save Users",
              command=lambda: [save_users_to_file(), messagebox.showinfo("Saved", "Users Saved!")]
).pack(fill="x", pady=5)

#Frame for user registration 
register_frame = ctk.CTkFrame(content_frame)

ctk.CTkLabel(register_frame, text="Register User", font=("Arial",18)).pack(pady=13)

name_entry = ctk.CTkEntry(register_frame, placeholder_text="Enter Name")
name_entry.pack(pady=5)

age_entry = ctk.CTkEntry(register_frame, placeholder_text="Enter Age")
age_entry.pack(pady=5)

role_combo = ctk.CTkComboBox(register_frame, values=["Student","Staff"])
role_combo.pack(pady=5)

submit_btn = ctk.CTkButton(register_frame,text="Submit", command=submit_user)
submit_btn.pack(pady=10)

#Frame for logging activity
activity_frame = ctk.CTkFrame(content_frame)

ctk.CTkLabel(activity_frame, text="Log Activity", font=("Arial",18)).pack(pady=10)

user_combo = ctk.CTkComboBox(activity_frame, values=[])
user_combo.pack(pady=5)

activity_combo = ctk.CTkComboBox(activity_frame,values=["Study", "Exercise", "Project", "Idle"])

activity_combo.set("Study")
activity_combo.pack(pady=5)

log_btn = ctk.CTkButton(activity_frame, text="Log Activity",command=submit_activity, state="disabled")
log_btn.pack(pady=10)

# Frame for Summary
ctk.CTkLabel(summary_frame, text="User Summary", font=("Arial",18)).pack(pady=10)

summary_container = ctk.CTkScrollableFrame(summary_frame, width=450, height=250)
summary_container.pack(pady=10, fill="both",expand=True)

load_users_from_files()
refresh_summary()
app.mainloop()






