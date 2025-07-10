import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection
import re
class PasswordValidationError(Exception):
    pass
def validate_password(password):
    pattern = r'^(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'
    if not re.match(pattern, password):
        raise PasswordValidationError("Password must be at least 8 characters long and contain at least one special character (!@#$%^&* etc.)")
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
def customer_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE email = %s AND password = %s", (email, password))
    customer = cursor.fetchone()
    conn.close()
    return customer
def register_customer(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customer (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        return True
    except Exception as e:
        return str(e)
    finally:
        conn.close()
def admin_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
    admin = cursor.fetchone()
    conn.close()
    return admin
class CustomerLogin:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.root = tk.Tk()
        self.root.title("Customer Login")
        self.root.geometry("400x350")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background="#FFFFFF", foreground="#333333")
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=8, background="#0E2A5B", foreground="white")
        self.create_login_page()
    def create_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        ttk.Label(header_frame, text="Customer Login", font=('Arial', 18, 'bold'), foreground="#0E2A5B").pack(pady=10)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        ttk.Label(main_frame, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(main_frame)
        self.email_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(pady=5)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Login", command=self.login, style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Register", command=self.show_register_page, style='TButton').pack(side=tk.RIGHT, padx=5)
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            validate_email(email)
            validate_password(password)
        except (PasswordValidationError, ValueError) as e:
            messagebox.showerror("Login Failed", str(e))
         customer = customer_login(email, password)
        if customer:
            messagebox.showinfo("Login Successful", "Welcome, Customer!")
            self.root.destroy()
            self.on_login_success(customer[0])
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")
    def register(self):
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        try:
            validate_email(email)
            validate_password(password)
            result = register_customer(email, password)
            if result is True:
                messagebox.showinfo("Registration Successful", "You can now log in.")
                self.create_login_page()
            else:
                messagebox.showerror("Registration Failed", result)
        except (PasswordValidationError, ValueError) as e:
            messagebox.showerror("Registration Failed", str(e))
    def show_register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        ttk.Label(header_frame, text="Customer Registration", font=('Arial', 18, 'bold'), foreground="#0E2A5B").pack(pady=10)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        ttk.Label(main_frame, text="Email:").pack(pady=5)
        self.register_email_entry = ttk.Entry(main_frame)
        self.register_email_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password:").pack(pady=5)
        self.register_password_entry = ttk.Entry(main_frame, show="*")
        self.register_password_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password must be at least 8 characters with special characters", font=('Arial', 8), foreground="#666666").pack(pady=5)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Register", command=self.register, style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Login", command=self.create_login_page, style='TButton').pack(side=tk.RIGHT, padx=5)
    def run(self):
        self.root.mainloop()
class AdminLogin:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.root = tk.Tk()
        self.root.title("Admin Login")
        self.root.geometry("500x500")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background="#FFFFFF", foreground="#333333")
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=8, background="#0E2A5B", foreground="white")
        self.create_login_page()
    def create_login_page(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        ttk.Label(header_frame, text="Admin Login", font=('Arial', 18, 'bold'), foreground="#0E2A5B").pack(pady=10)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        ttk.Label(main_frame, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(main_frame)
        self.email_entry.pack(pady=5)
        ttk.Label(main_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(pady=5)
        ttk.Button(main_frame, text="Login", command=self.login, style='TButton').pack(pady=20)
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        try:
            validate_email(email)
            validate_password(password)
        except (PasswordValidationError, ValueError) as e:
            messagebox.showerror("Login Failed", str(e))
            return
        admin = admin_login(email, password)
        if admin:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")
    def run(self):
        self.root.mainloop()