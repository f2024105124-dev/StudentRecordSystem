import tkinter as tk
from tkinter import messagebox

STUDENT_DB = {}
next_roll_no = 1;

def add_student_record(name, father_name, class_name, marks):
    global next_roll_no
    STUDENT_DB[next_roll_no] = {
        "name": name,
        "father_name": father_name,
        "class_name": class_name,
        "marks": marks,
    }
    next_roll_no += 1


def update_student_record(roll_no, name, father_name, class_name, marks):
    if roll_no in STUDENT_DB:
        STUDENT_DB[roll_no] = {
            "name": name,
            "father_name": father_name,
            "class_name": class_name,
            "marks": marks,
        }
        return True
    return False


def delete_student_record(roll_no):
    if roll_no in STUDENT_DB:
        del STUDENT_DB[roll_no]
        return True
    return False


class SimpleStudentApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("650x550")

        title_lbl = tk.Label(
            root,
            text="STUDENT RECORD MANAGEMENT SYSTEM",
            font=("Arial", 14, "bold"),
            pady=10,
        )
        title_lbl.pack()

        form_frame = tk.LabelFrame(
            root, text=" Student Information Form ", padx=15, pady=10
        )
        form_frame.pack(pady=10, fill=tk.X, padx=20)

        # Labels & Entry Boxes
        tk.Label(form_frame, text="Roll No (For Update/Delete/Search):").grid(
            row=0, column=0, sticky="w"
        )
        self.ent_roll = tk.Entry(form_frame, width=10)
        self.ent_roll.grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(form_frame, text="Student Name:").grid(
            row=1, column=0, sticky="w"
        )
        self.ent_name = tk.Entry(form_frame, width=30)
        self.ent_name.grid(row=1, column=1, pady=2)

        tk.Label(form_frame, text="Father's Name:").grid(
            row=2, column=0, sticky="w"
        )
        self.ent_father = tk.Entry(form_frame, width=30)
        self.ent_father.grid(row=2, column=1, pady=2)

        tk.Label(form_frame, text="Class:").grid(row=3, column=0, sticky="w")
        self.ent_class = tk.Entry(form_frame, width=30)
        self.ent_class.grid(row=3, column=1, pady=2)

        tk.Label(form_frame, text="Marks:").grid(row=4, column=0, sticky="w")
        self.ent_marks = tk.Entry(form_frame, width=30)
        self.ent_marks.grid(row=4, column=1, pady=2)

        # --- FRAME FOR ACTION BUTTONS ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Student",
            width=12,
            bg="#d4edda",
            command=self.add_student,
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            btn_frame,
            text="View All",
            width=12,
            bg="#e2e3e5",
            command=self.view_students,
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            btn_frame,
            text="Search Roll",
            width=12,
            bg="#cce5ff",
            command=self.search_student,
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            btn_frame,
            text="Update Record",
            width=12,
            bg="#fff3cd",
            command=self.update_student,
        ).grid(row=0, column=3, padx=5)
        tk.Button(
            btn_frame,
            text="Delete Record",
            width=12,
            bg="#f8d7da",
            command=self.delete_student,
        ).grid(row=0, column=4, padx=5)

        display_frame = tk.LabelFrame(root, text=" Records Display Board ")
        display_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.scrollbar = tk.Scrollbar(display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_display = tk.Text(
            display_frame,
            font=("Courier", 10),
            yscrollcommand=self.scrollbar.set,
        )
        self.txt_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.txt_display.yview)

        # Show an initial empty state view
        self.clear_form()
        self.view_students()

    def clear_form(self):
        """Clears text out of all entry widgets"""
        self.ent_roll.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_father.delete(0, tk.END)
        self.ent_class.delete(0, tk.END)
        self.ent_marks.delete(0, tk.END)

    def add_student(self):
        name = self.ent_name.get().strip()
        father = self.ent_father.get().strip()
        class_name = self.ent_class.get().strip()
        marks_raw = self.ent_marks.get().strip()

        if not (name and father and class_name and marks_raw):
            messagebox.showwarning(
                "Missing Data",
                "Please fill Name, Father Name, Class, and Marks.",
            )
            return

        try:
            marks = float(marks_raw)
        except ValueError:
            messagebox.showerror("Error", "Marks must be a valid number.")
            return

        add_student_record(name, father, class_name, marks)
        messagebox.showinfo("Success", "Student record saved!")
        self.clear_form()
        self.view_students()

    def view_students(self):
        """Formats records into a clean text string and displays them"""
        self.txt_display.delete("1.0", tk.END)

        if not STUDENT_DB:
            self.txt_display.insert(tk.END, "No records found in the system.")
            return

        header = f"{'Roll No':<10}{'Name':<15}{'Father Name':<15}{'Class':<10}{'Marks':<10}\n"
        divider = "-" * 60 + "\n"
        self.txt_display.insert(tk.END, header + divider)

        for roll_no, data in STUDENT_DB.items():
            row = f"{roll_no:<10}{data['name']:<15}{data['father_name']:<15}{data['class_name']:<10}{data['marks']:<10}\n"
            self.txt_display.insert(tk.END, row)

    def search_student(self):
        roll_raw = self.ent_roll.get().strip()
        if not roll_raw:
            messagebox.showwarning(
                "Input Required", "Please enter a Roll No to search."
            )
            return

        try:
            roll_no = int(roll_raw)
        except ValueError:
            messagebox.showerror("Error", "Roll No must be an integer number.")
            return

        self.txt_display.delete("1.0", tk.END)
        if roll_no in STUDENT_DB:
            data = STUDENT_DB[roll_no]
            result = (
                f"Student Record Found:\n"
                f"---------------------\n"
                f"Roll No     : {roll_no}\n"
                f"Name        : {data['name']}\n"
                f"Father Name : {data['father_name']}\n"
                f"Class       : {data['class_name']}\n"
                f"Marks       : {data['marks']}\n"
            )
            self.txt_display.insert(tk.END, result)
        else:
            self.txt_display.insert(
                tk.END, f"Roll No {roll_no} does not exist."
            )

    def update_student(self):
        roll_raw = self.ent_roll.get().strip()
        if not roll_raw:
            messagebox.showwarning(
                "Input Required", "Enter Roll No to identify the target record."
            )
            return

        try:
            roll_no = int(roll_raw)
        except ValueError:
            messagebox.showerror("Error", "Roll No must be an integer.")
            return

        if roll_no not in STUDENT_DB:
            messagebox.showerror("Error", "This Roll No does not exist.")
            return

        old_data = STUDENT_DB[roll_no]
        name = self.ent_name.get().strip() or old_data["name"]
        father = self.ent_father.get().strip() or old_data["father_name"]
        class_name = self.ent_class.get().strip() or old_data["class_name"]
        marks_raw = self.ent_marks.get().strip()

        if marks_raw:
            try:
                marks = float(marks_raw)
            except ValueError:
                messagebox.showerror("Error", "Marks must be a valid number.")
                return
        else:
            marks = old_data["marks"]

        update_student_record(roll_no, name, father, class_name, marks)
        messagebox.showinfo("Success", f"Record for Roll No {roll_no} updated!")
        self.clear_form()
        self.view_students()

    def delete_student(self):
        roll_raw = self.ent_roll.get().strip()
        if not roll_raw:
            messagebox.showwarning("Input Required", "Enter Roll No to delete.")
            return

        try:
            roll_no = int(roll_raw)
        except ValueError:
            messagebox.showerror("Error", "Roll No must be an integer.")
            return

        if roll_no not in STUDENT_DB:
            messagebox.showerror("Error", "This Roll No does not exist.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Roll No {roll_no}?",
        )
        if confirm:
            delete_student_record(roll_no)
            messagebox.showinfo("Deleted", "Record removed successfully.")
            self.clear_form()
            self.view_students()


if __name__ == "__main__":
    window = tk.Tk()
    app = SimpleStudentApp(window)
    window.mainloop()
