import tkinter as tk
import requests
import datetime
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from fpdf import FPDF
import os
from database import *
from admin_login import AdminLogin
from customer_login import CustomerLogin
from datetime import datetime
class CelestiaAirlinesApp:
    API_KEY = '606a419df38bff95986c9f4745721ac5'  # Weather API key
    CRITICAL_CONDITIONS = ['thunderstorm', 'heavy rain', 'snow', 'hurricane', 'tornado']
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Celestia Airlines")
        self.root.geometry("800x600")  # Smaller window size
        self.setup_styles()
        self.book_btn = None 
        self.seat_buttons = {}  # To store seat button references
        self.current_selected_seat = None  # To track currently selected seat
        self.selected_seat = tk.StringVar() # Initialize book_btn
        self.show_main_menu()
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.primary_color = "#0E2A5B"  # Dark blue
        self.secondary_color = "#FF6B00"  # Orange
        self.bg_color = "#FFFFFF"       # White
        self.text_color = "#333333"     # Dark gray
        self.highlight_color = "#F5F5F5" # Light gray
        self.style.configure('.', background=self.bg_color,foreground=self.text_color)
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=8, background=self.primary_color,foreground="white",borderwidth=0)
        self.style.map('TButton', background=[('active', self.secondary_color),('disabled', '#CCCCCC')])
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'),foreground=self.primary_color)
        self.style.configure('Subheader.TLabel',font=('Arial', 14),foreground=self.primary_color)        
        self.style.configure('TFrame',background=self.bg_color)        
        self.style.configure('TEntry',fieldbackground="white",foreground=self.text_color,
                           bordercolor=self.primary_color,lightcolor=self.primary_color,padding=5)
        self.style.configure('TCombobox',selectbackground=self.highlight_color)
        self.style.configure('Treeview',background="white",fieldbackground="white",foreground=self.text_color)
        self.style.map('Treeview',background=[('selected', self.secondary_color)])
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.attributes('-fullscreen', True)   
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=(20, 10))
        ttk.Label(header_frame, 
                 text="✈ Celestia Airlines", 
                 style='Header.TLabel').pack(pady=10)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        ttk.Label(main_frame, text="Book, Manage, Fly", style='Subheader.TLabel').pack(pady=10)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        admin_btn = ttk.Button(btn_frame, text="Admin Login", command=self.show_admin_login,style='TButton',width=20)
        admin_btn.pack(pady=15, ipady=10)
        customer_btn = ttk.Button(btn_frame, text="Customer Login", 
                                command=self.show_customer_login,style='TButton',width=20)
        customer_btn.pack(pady=15, ipady=10)
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, pady=(10, 20))
        ttk.Label(footer_frame, text="© 2023 Celestia Airlines. All rights reserved.", font=('Arial', 8)).pack()
    def show_admin_login(self):
        admin_login = AdminLogin(self.show_admin_dashboard)
        admin_login.run()
    def show_customer_login(self):
        customer_login = CustomerLogin(lambda id, name: self.show_customer_dashboard(id, name))
        customer_login.run()
    def show_admin_dashboard(self):
        self.root.geometry("1200x800")  # Larger window for better layout
        for widget in self.root.winfo_children():
            widget.destroy()
        main_container = ttk.Frame(self.root)# Main container
        main_container.pack(fill=tk.BOTH, expand=True)
        sidebar_frame = ttk.Frame(main_container, width=200)# Sidebar Frame
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.admin_content_frame = ttk.Frame(main_container)# Main Content Frame
        self.admin_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(sidebar_frame, text="Flight Management", style='Subheader.TLabel').pack(pady=10)# Sidebar Buttons
        buttons = [("Add Flight", self.show_add_flight),
            ("View Flights", self.show_view_flights),
            ("Cancel Flight", self.show_cancel_flight),
            ("Weather Check", self.show_weather_check),
            ("Crew Management", self.show_crew_management),
            ("Pilot Management", self.show_pilot_management)]
        for text, command in buttons:
            btn = ttk.Button(sidebar_frame, text=text, command=command, width=20)
            btn.pack(pady=5)
        ttk.Button(sidebar_frame,text="Logout",command=self.show_main_menu).pack(side=tk.BOTTOM, pady=20)
        self.show_view_flights()
    def clear_admin_content(self):
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()
    def show_add_flight(self):
        self.clear_admin_content()
        form_frame = ttk.Frame(self.admin_content_frame)
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        cities_of_india = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad",
            "Chennai", "Kolkata", "Surat", "Pune", "Jaipur","Thane", "Bhopal", 
            "Lucknow", "Kanpur", "Nagpur", "Visakhapatnam", "Indore","Patna", "Vadodara", "Ghaziabad"]
        left_frame = ttk.Frame(form_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        right_frame = ttk.Frame(form_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        ttk.Label(left_frame, text="Source:").pack(pady=5)
        source_var = tk.StringVar(value=cities_of_india[0])
        ttk.OptionMenu(left_frame, source_var, *cities_of_india).pack(fill=tk.X)
        ttk.Label(left_frame, text="Destination:").pack(pady=5)
        dest_var = tk.StringVar(value=cities_of_india[1])
        ttk.OptionMenu(left_frame, dest_var, *cities_of_india).pack(fill=tk.X)
        ttk.Label(left_frame, text="Departure Date:").pack(pady=5)
        cal = Calendar(left_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)
        ttk.Label(left_frame, text="Departure Time (HH:MM):").pack()
        departure_time_entry = ttk.Entry(left_frame)
        departure_time_entry.pack(fill=tk.X)
        ttk.Label(left_frame, text="Arrival Time (HH:MM):").pack()
        arrival_time_entry = ttk.Entry(left_frame)
        arrival_time_entry.pack(fill=tk.X)
        ttk.Label(right_frame, text="Economy Price (₹):").pack()
        economy_price_entry = ttk.Entry(right_frame)
        economy_price_entry.pack(fill=tk.X, pady=5)
        ttk.Label(right_frame, text="Business Price (₹):").pack()
        business_price_entry = ttk.Entry(right_frame)
        business_price_entry.pack(fill=tk.X, pady=5)
        ttk.Label(right_frame, text="First Class Price (₹):").pack()
        first_class_price_entry = ttk.Entry(right_frame)
        first_class_price_entry.pack(fill=tk.X, pady=5)
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=20, fill=tk.X)
        ttk.Button(btn_frame, text="Add Flight", command=lambda: perform_add()).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.clear_admin_content).pack(side=tk.RIGHT, padx=5)
        def perform_add():
            source = source_var.get()
            destination = dest_var.get()
            date = cal.get_date()
            dep_time = departure_time_entry.get()
            arr_time = arrival_time_entry.get()
            try:
                economy = float(economy_price_entry.get())
                business = float(business_price_entry.get())
                first = float(first_class_price_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid prices.")
                return
            if not all([source, destination, date, dep_time, arr_time]):
                messagebox.showerror("Error", "All fields must be filled!")
                return
            if source == destination:
                messagebox.showerror("Error", "Source and Destination cannot be the same.")
                return
            if economy <= 0 or business <= 0 or first <= 0:
                messagebox.showerror("Error", "Prices must be positive.")
                return
            success, error = add_flight(source=source,destination=destination,departure_date=date,
                departure_time=dep_time,arrival_time=arr_time,
                economy_price=economy,business_price=business,first_class_price=first)  # simulate success
            if success:
                messagebox.showinfo("Success", "Flight added successfully!")
                self.clear_admin_content()
            else:
                messagebox.showerror("Error", error or "Failed to add flight.")
    def generate_ticket_from_selection(self):
        selected_item = self.bookings_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking first!")
            return
        booking_id = self.bookings_tree.item(selected_item)['values'][0]
        self.generate_ticket_pdf_by_booking(booking_id)
    def cancel_selected_booking(self):
        selected_item = self.bookings_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking first!")
            return
        booking_id = self.bookings_tree.item(selected_item)['values'][0]
        success = cancel_ticket(booking_id)
        if success:
            messagebox.showinfo("Success", "Booking cancelled successfully!")
            self.view_bookings(self.current_customer_id)
        else:
            messagebox.showerror("Error", "Failed to cancel booking")
    def show_view_flights(self):
        self.clear_admin_content()
        view_frame = ttk.Frame(self.admin_content_frame)
        view_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tree_frame = ttk.Frame(view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,show="headings",
                columns=("id", "source", "dest", "date", "dep_time", "arriv_time", "econ_price", "bus_price", "first_price"))
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.heading("dep_time", text="Departure")
        tree.heading("arriv_time", text="Arrival")
        tree.heading("econ_price", text="Economy Price")
        tree.heading("bus_price", text="Business Price")
        tree.heading("first_price", text="First Class Price")
        tree.column("id", width=80)
        tree.column("source", width=100)
        tree.column("dest", width=100)
        tree.column("date", width=100)
        tree.column("dep_time", width=100)
        tree.column("arriv_time", width=100)
        tree.column("econ_price", width=100)
        tree.column("bus_price", width=100)
        tree.column("first_price", width=100)
        tree.pack(fill=tk.BOTH, expand=True)        # Load data
        flights = get_all_flights()
        for flight in flights:
            tree.insert("", tk.END, values=(flight[0], flight[1], flight[2], flight[3],
                flight[4], flight[5], f"₹{flight[8]}", f"₹{flight[9]}", f"₹{flight[10]}"))
    def show_cancel_flight(self):
        self.clear_admin_content()
        cancel_frame = ttk.Frame(self.admin_content_frame)
        cancel_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tree_frame = ttk.Frame(cancel_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame,yscrollcommand=scrollbar.set,
                    columns=("id", "source", "dest", "date"),show="headings",selectmode="browse")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.pack(fill=tk.BOTH, expand=True)
        flights = get_all_flights()
        for flight in flights:
            tree.insert("", tk.END, values=(flight[0], flight[1], flight[2], flight[3]))
        def perform_cancellation():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a flight from the list!")
                return
            flight_id = tree.item(selected_item)['values'][0]
            success, error_message = cancel_flight(flight_id)
            if success:
                messagebox.showinfo("Success", f"Flight {flight_id} cancelled successfully!")
                self.show_view_flights()  # Refresh the view
            else:
                messagebox.showerror("Error", error_message)
        btn_frame = ttk.Frame(cancel_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cancel Selected Flight", 
                  command=perform_cancellation,style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.clear_admin_content).pack(side=tk.RIGHT, padx=5)
    def show_weather_check(self):
        self.clear_admin_content()
        weather_frame = ttk.Frame(self.admin_content_frame)
        weather_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        ttk.Label(weather_frame, text="Flight Weather Monitoring", style='Subheader.TLabel').pack(pady=10)
        tree_container = ttk.Frame(weather_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = ttk.Scrollbar(tree_container)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.weather_flight_tree = ttk.Treeview(tree_container,xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set,columns=("id", "source", "date"),show="headings",height=8 )
        self.weather_flight_tree.pack(fill=tk.BOTH, expand=True)
        x_scrollbar.config(command=self.weather_flight_tree.xview)
        y_scrollbar.config(command=self.weather_flight_tree.yview)
        self.weather_flight_tree.heading("id", text="Flight ID", anchor=tk.CENTER)
        self.weather_flight_tree.heading("source", text="Source City", anchor=tk.CENTER)
        self.weather_flight_tree.heading("date", text="Date", anchor=tk.CENTER)
        self.weather_flight_tree.column("id", width=150, anchor=tk.CENTER)
        self.weather_flight_tree.column("source", width=200, anchor=tk.CENTER)
        self.weather_flight_tree.column("date", width=200, anchor=tk.CENTER)
        self.weather_labels = {'city': ttk.Label(weather_frame, text="", font=('Arial', 10)),
            'temp': ttk.Label(weather_frame, text="", font=('Arial', 10)),
            'condition': ttk.Label(weather_frame, text="", font=('Arial', 10)),
            'warning': ttk.Label(weather_frame, text="", foreground="red", font=('Arial', 10, 'bold'))}
        for label in self.weather_labels.values():
            label.pack(pady=5)
        self.weather_btn_frame = ttk.Frame(weather_frame)
        self.weather_btn_frame.pack(pady=10)
        ttk.Button(self.weather_btn_frame, text="Check Weather", command=self.check_flight_weather).pack(side=tk.LEFT, padx=5)
        self.delay_btn = ttk.Button(self.weather_btn_frame, text="Delay Flight", 
                                   command=self.delay_flight,state=tk.DISABLED)
        self.cancel_btn = ttk.Button(self.weather_btn_frame, text="Cancel Flight", 
                                    command=self.cancel_flight_weather,state=tk.DISABLED)
        self.delay_btn.pack(side=tk.LEFT, padx=5)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        self.load_upcoming_flights()
    def show_crew_management(self):
        self.clear_admin_content()
        crew_frame = ttk.Frame(self.admin_content_frame)
        crew_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        ttk.Label(crew_frame, text="Crew Management", style='Subheader.TLabel').pack(pady=10)
        ttk.Button(crew_frame, text="Add Crew", command=self.add_crew).pack(pady=5)
        ttk.Button(crew_frame, text="View Crew", command=self.view_crew).pack(pady=5)
        ttk.Button(crew_frame, text="Remove Crew", command=self.remove_crew).pack(pady=5)
    def show_pilot_management(self):
        self.clear_admin_content()
        pilot_frame = ttk.Frame(self.admin_content_frame)
        pilot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        ttk.Label(pilot_frame, text="Pilot Management", style='Subheader.TLabel').pack(pady=10)
        ttk.Button(pilot_frame, text="Add Pilot", command=self.add_pilots).pack(pady=5)
        ttk.Button(pilot_frame, text="View Pilots", command=self.view_pilots).pack(pady=5)
        ttk.Button(pilot_frame, text="Remove Pilot", command=self.remove_pilots).pack(pady=5)
    def show_customer_dashboard(self, customer_id, customer_name):
        self.current_customer_id = customer_id
        self.customer_name = customer_name
        self.root.geometry("1000x800")
        for widget in self.root.winfo_children():
            widget.destroy()
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=(10, 20))
        ttk.Label(header_frame, text="Customer Dashboard", style='Header.TLabel').pack(pady=10)
        ttk.Label(header_frame, text=f"Welcome, {customer_name}", style='Header.TLabel').pack(pady=10)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        search_book_frame = ttk.Frame(notebook)# ===== Search & Book Tab =====
        notebook.add(search_book_frame, text="Search & Book")
        sb_container = ttk.Frame(search_book_frame)# Scrollable Container
        sb_container.pack(fill=tk.BOTH, expand=True)
        sb_canvas = tk.Canvas(sb_container)
        sb_scrollbar = ttk.Scrollbar(sb_container, orient="vertical", command=sb_canvas.yview)
        sb_scrollable_frame = ttk.Frame(sb_canvas)
        sb_scrollable_frame.bind("<Configure>", lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))
        sb_canvas.create_window((0, 0), window=sb_scrollable_frame, anchor="nw")
        sb_canvas.configure(yscrollcommand=sb_scrollbar.set)
        sb_canvas.pack(side="left", fill="both", expand=True)
        sb_scrollbar.pack(side="right", fill="y")
        search_frame = ttk.LabelFrame(sb_scrollable_frame, text="Search Flights", padding=10)# Search Section
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        trip_type_frame = ttk.Frame(search_frame)# Trip type
        trip_type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(trip_type_frame, text="Trip Type:").pack(side=tk.LEFT)
        self.trip_type = tk.StringVar(value="ONE WAY")
        ttk.Radiobutton(trip_type_frame, text="ONE WAY", variable=self.trip_type, value="ONE WAY").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(trip_type_frame, text="ROUND TRIP", variable=self.trip_type, value="ROUND TRIP").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(trip_type_frame, text="MULTI CITY", variable=self.trip_type, value="MULTI CITY").pack(side=tk.LEFT, padx=5)
        loc_frame = ttk.Frame(search_frame) # From/To
        loc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(loc_frame, text="From:").grid(row=0, column=0, sticky=tk.W)
        self.from_city = ttk.Combobox(loc_frame, values=["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
            "Kolkata", "Ahmedabad", "Pune", "Jaipur", "Lucknow"])
        self.from_city.grid(row=1, column=0, padx=5, sticky=tk.W+tk.E)
        ttk.Label(loc_frame, text="To:").grid(row=0, column=1, sticky=tk.W)
        self.to_city = ttk.Combobox(loc_frame, values=["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
            "Kolkata", "Ahmedabad", "Pune", "Jaipur", "Lucknow"])
        self.to_city.grid(row=1, column=1, padx=5, sticky=tk.W+tk.E)    
        ttk.Button(search_frame,text="SEARCH FLIGHTS",command=lambda: self.perform_search(customer_id),style='TButton').pack(pady=10)
        results_frame = ttk.LabelFrame(sb_scrollable_frame, text="Available Flights", padding=10)# Results Section
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.flights_tree = ttk.Treeview(tree_frame, show="headings",yscrollcommand=scrollbar.set,
            columns=("id", "source", "dest", "date", "dep_time", "arriv_time", "econ_price", "bus_price"))
        scrollbar.config(command=self.flights_tree.yview)
        for col in ["id", "source", "dest", "date", "dep_time", "arriv_time", "econ_price", "bus_price"]:
            self.flights_tree.heading(col, text=col.replace('_', ' ').title())
            self.flights_tree.column(col, width=100)
        self.flights_tree.pack(fill=tk.BOTH, expand=True)
        self.book_btn = ttk.Button(results_frame, text="BOOK SELECTED FLIGHT", style='TButton',
                                 command=lambda: self.book_selected_flight(customer_id))
        self.book_btn.pack(pady=10)
        book_frame = ttk.Frame(notebook)# ===== Direct Booking Tab =====
        notebook.add(book_frame, text="Direct Booking")
        db_container = ttk.Frame(book_frame)# Scrollable Container
        db_container.pack(fill=tk.BOTH, expand=True)
        db_canvas = tk.Canvas(db_container)
        db_scrollbar = ttk.Scrollbar(db_container, orient="vertical", command=db_canvas.yview)
        db_scrollable_frame = ttk.Frame(db_canvas)
        db_scrollable_frame.bind("<Configure>", lambda e: db_canvas.configure(scrollregion=db_canvas.bbox("all")))
        db_canvas.create_window((0, 0), window=db_scrollable_frame, anchor="nw")
        db_canvas.configure(yscrollcommand=db_scrollbar.set)
        db_canvas.pack(side="left", fill="both", expand=True)
        db_scrollbar.pack(side="right", fill="y")
        flight_id_frame = ttk.Frame(db_scrollable_frame)# Flight ID Section
        flight_id_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(flight_id_frame, text="Flight ID:").pack(side=tk.LEFT)
        self.book_flight_entry = ttk.Entry(flight_id_frame)
        self.book_flight_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(flight_id_frame, text="Show Available Seats", style='TButton',
                  command=lambda: self.show_seats_for_booking(book_frame, customer_id)).pack(side=tk.RIGHT, padx=5)
        class_frame = ttk.LabelFrame(db_scrollable_frame, text="Class Selection", padding=10)# Class Selection
        class_frame.pack(fill=tk.X, padx=20, pady=10)
        self.class_var = tk.StringVar(value="economy")
        ttk.Radiobutton(class_frame, text="Economy", variable=self.class_var, value="economy").pack(anchor=tk.W)
        ttk.Radiobutton(class_frame, text="Business", variable=self.class_var, value="business").pack(anchor=tk.W)
        ttk.Radiobutton(class_frame, text="First Class", variable=self.class_var, value="first_class").pack(anchor=tk.W)
        self.seat_frame = ttk.LabelFrame(db_scrollable_frame, text="Seat Selection", padding=10)# Seat Selection
        self.seat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(self.seat_frame)
        scrollbar = ttk.Scrollbar(self.seat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.seat_grid_frame = ttk.Frame(self.scrollable_frame)
        self.seat_grid_frame.pack(fill=tk.BOTH, expand=True)
        self.selected_seat = tk.StringVar()
        details_frame = ttk.LabelFrame(db_scrollable_frame, text="Passenger Details", padding=10)# Passenger Details
        details_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(details_frame, text="Passenger Name:").pack()
        self.name_entry = ttk.Entry(details_frame)
        self.name_entry.pack(pady=5)
        ttk.Button(db_scrollable_frame, text="Confirm Booking", 
                  command=lambda: self.perform_booking_from_tab(customer_id),style='TButton').pack(pady=10)
        bookings_frame = ttk.Frame(notebook)# ===== My Bookings Tab =====
        notebook.add(bookings_frame, text="My Bookings")
        mb_container = ttk.Frame(bookings_frame)# Scrollable Container
        mb_container.pack(fill=tk.BOTH, expand=True)
        mb_canvas = tk.Canvas(mb_container)
        mb_scrollbar = ttk.Scrollbar(mb_container, orient="vertical", command=mb_canvas.yview)
        mb_scrollable_frame = ttk.Frame(mb_canvas)
        mb_scrollable_frame.bind("<Configure>", lambda e: mb_canvas.configure(scrollregion=mb_canvas.bbox("all")))
        mb_canvas.create_window((0, 0), window=mb_scrollable_frame, anchor="nw")
        mb_canvas.configure(yscrollcommand=mb_scrollbar.set)
        mb_canvas.pack(side="left", fill="both", expand=True)
        mb_scrollbar.pack(side="right", fill="y")
        bookings_tree_frame = ttk.Frame(mb_scrollable_frame)# Bookings Treeview
        bookings_tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        scrollbar = ttk.Scrollbar(bookings_tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bookings_tree = ttk.Treeview(bookings_tree_frame, 
            columns=("id", "flight_id", "source", "dest", "date", "seat", "class"),show="headings",yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.bookings_tree.yview)
        for col in ["id", "flight_id", "source", "dest", "date", "seat", "class"]:
            self.bookings_tree.heading(col, text=col.title())
            self.bookings_tree.column(col, width=100)
        self.bookings_tree.pack(fill=tk.BOTH, expand=True)
        bookings_btn_frame = ttk.Frame(mb_scrollable_frame)
        bookings_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(bookings_btn_frame, text="Refresh Bookings", command=lambda: self.view_bookings(customer_id)).pack(side=tk.LEFT)
        ttk.Button(bookings_btn_frame, text="Generate PDF Ticket", command=self.generate_ticket_from_selection).pack(side=tk.LEFT)
        ttk.Button(bookings_btn_frame, text="Cancel Booking", command=self.cancel_selected_booking).pack(side=tk.LEFT)
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, pady=(10, 20))
        ttk.Button(footer_frame, text="Logout", command=self.show_main_menu).pack(pady=10)
        self.view_bookings(customer_id)
    def _bind_to_mousewheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    def _unbind_from_mousewheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")
    def load_upcoming_flights(self):
        for item in self.weather_flight_tree.get_children():
            self.weather_flight_tree.delete(item)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT id, source, departure_date FROM flights 
                WHERE departure_date >= CURDATE() ORDER BY departure_date ASC""")
            flights = cursor.fetchall()
            for flight in flights:
                self.weather_flight_tree.insert("", tk.END, values=(flight[0], flight[1], flight[2]))
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            if conn.is_connected():
                conn.close()
    def check_flight_weather(self):
        selected = self.weather_flight_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a flight first!")
            return
        flight_id = self.weather_flight_tree.item(selected)['values'][0]
        city = self.weather_flight_tree.item(selected)['values'][1]
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self.API_KEY}"
            response = requests.get(url)
            data = response.json()
            if data['cod'] != 200:
                raise Exception(data['message'])
            weather = {'city': data['name'],
                'temp': data['main']['temp'],
                'condition': data['weather'][0]['main'].lower(),
                'description': data['weather'][0]['description'].lower()}
            self.weather_labels['city'].config(text=f"City: {weather['city']}")
            self.weather_labels['temp'].config(text=f"Temperature: {weather['temp']}°C")
            self.weather_labels['condition'].config(text=f"Condition: {weather['description'].title()}")
            is_critical = any(cond in weather['description'] for cond in self.CRITICAL_CONDITIONS)
            if is_critical:
                self.weather_labels['warning'].config(
                    text="WARNING: Critical weather detected! Consider delaying or canceling the flight.")
                self.delay_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.NORMAL)
            else:
                self.weather_labels['warning'].config(text="Weather conditions are normal")
                self.delay_btn.config(state=tk.DISABLED)
                self.cancel_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Weather Error", f"Failed to get weather data: {str(e)}")
    def delay_flight(self):
        selected = self.weather_flight_tree.selection()
        flight_id = self.weather_flight_tree.item(selected)['values'][0]
        messagebox.showinfo("Flight Delayed", f"Flight {flight_id} has been delayed")
        self.load_upcoming_flights()
        self.clear_weather_display()
    def cancel_flight_weather(self):
        selected = self.weather_flight_tree.selection()
        flight_id = self.weather_flight_tree.item(selected)['values'][0]
        success, error_message = cancel_flight(flight_id)
        if success:
            messagebox.showinfo("Success", f"Flight {flight_id} cancelled successfully!")
            self.load_upcoming_flights()
            self.clear_weather_display()
        else:
            messagebox.showerror("Error", error_message)
    def clear_weather_display(self):
        for label in self.weather_labels.values():
            label.config(text="")
        self.weather_labels['warning'].config(text="")
        self.delay_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
    def add_flight(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Flight")
        add_window.geometry("500x600")
        main_frame = ttk.Frame(add_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        cities_of_india = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad","Nagpur", "Visakhapatnam",
            "Chennai", "Kolkata", "Surat", "Pune", "Jaipur","Lucknow", "Kanpur","Indore",
            "Thane", "Bhopal", "Patna", "Vadodara", "Ghaziabad"]
        ttk.Label(main_frame, text="Source:").pack(pady=5)
        source_var = tk.StringVar(value=cities_of_india[0])
        ttk.OptionMenu(main_frame, source_var, *cities_of_india).pack()
        ttk.Label(main_frame, text="Destination:").pack(pady=5)
        dest_var = tk.StringVar(value=cities_of_india[0])
        ttk.OptionMenu(main_frame, dest_var, *cities_of_india).pack()
        ttk.Label(main_frame, text="Departure Date:").pack(pady=5)
        cal = Calendar(main_frame, selectmode='day',date_pattern='yyyy-mm-dd',year=2025, month=4, day=3)
        cal.pack(pady=10)
        ttk.Label(main_frame, text="Departure Time (HH:MM):").pack()
        departure_time_entry = ttk.Entry(main_frame)
        departure_time_entry.pack()
        ttk.Label(main_frame, text="Arrival Time (HH:MM):").pack()
        arrival_time_entry = ttk.Entry(main_frame)
        arrival_time_entry.pack()
        ttk.Label(main_frame, text="Economy Price (₹):").pack()
        economy_price_entry = ttk.Entry(main_frame)
        economy_price_entry.pack()
        ttk.Label(main_frame, text="Business Price (₹):").pack()
        business_price_entry = ttk.Entry(main_frame)
        business_price_entry.pack()
        ttk.Label(main_frame, text="First Class Price (₹):").pack()
        first_class_price_entry = ttk.Entry(main_frame)
        first_class_price_entry.pack()
        def perform_add():
            source = source_var.get()
            dest = dest_var.get()
            date = cal.get_date()
            departure_time = departure_time_entry.get()
            arrival_time = arrival_time_entry.get()
            try:
                economy_price = float(economy_price_entry.get())
                business_price = float(business_price_entry.get())
                first_class_price = float(first_class_price_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Prices must be valid numbers")
                return
            if not all([source, dest, date,departure_time,arrival_time]):
                messagebox.showerror("Error", "All fields are required!")
                return
            if any(price <= 0 for price in [economy_price, business_price, first_class_price]):
                messagebox.showerror("Error", "Prices must be positive numbers")
                return
            result = add_flight(source=source,destination=dest,departure_date=date,departure_time=departure_time,
            arrival_time=arrival_time,economy_price=economy_price,business_price=business_price,first_class_price=first_class_price)
            if result is True:
                messagebox.showinfo("Success", "Flight added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror("Error", result)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Add Flight", command=perform_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=add_window.destroy).pack(side=tk.RIGHT, padx=5)
    def view_flights(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Flights")
        view_window.geometry("800x500")
        main_frame = ttk.Frame(view_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        flights = get_all_flights()
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,show="headings",
        columns=("id", "source", "dest", "date", "dep_time", "arriv_time", "econ_price", "bus_price", "first_price"))
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.heading("dep_time", text="Departure Time")
        tree.heading("arriv_time", text="Arrival Time")
        tree.heading("econ_price", text="Economy Price")
        tree.heading("bus_price", text="Business Price")
        tree.heading("first_price", text="First Class Price")
        tree.column("id", width=80)
        tree.column("source", width=100)
        tree.column("dest", width=100)
        tree.column("date", width=120)
        tree.column("econ_price", width=100)
        tree.column("bus_price", width=100)
        tree.column("first_price", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        for flight in flights:
            tree.insert("", tk.END, values=(flight[0], flight[1], flight[2], flight[3], f"₹{flight[7]}", f"₹{flight[8]}", f"₹{flight[9]}"))
    def add_pilots(self):
        add_pilots = tk.Toplevel(self.root)
        add_pilots.title("Add Pilots")
        add_pilots.geometry("400x400")
        main_frame = ttk.Frame(add_pilots)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        ttk.Label(main_frame, text="Name:").pack()
        name_entry = ttk.Entry(main_frame)
        name_entry.pack(pady=5)
        ttk.Label(main_frame, text="Age:").pack()
        age_entry = ttk.Entry(main_frame)
        age_entry.pack(pady=5)
        def perform_add_pilots():  
            name = name_entry.get()
            age = age_entry.get()
            result = add_pilot(name, age)
            if result is True:
                messagebox.showinfo("Success", "Pilot added successfully!")
                add_pilots.destroy()
            else:
                messagebox.showerror("Error", result)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add", command=perform_add_pilots).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=add_pilots.destroy).pack(side=tk.RIGHT, padx=5)
    def add_crew(self):
        add_crew_window = tk.Toplevel(self.root)  
        add_crew_window.title("Add Crew Members")  
        add_crew_window.geometry("400x400")
        main_frame = ttk.Frame(add_crew_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        ttk.Label(main_frame, text="Name:").pack()
        name_entry = ttk.Entry(main_frame)
        name_entry.pack(pady=5)
        ttk.Label(main_frame, text="Age:").pack()
        age_entry = ttk.Entry(main_frame)
        age_entry.pack(pady=5)
        def perform_add_crew():  
            name = name_entry.get()
            age = age_entry.get()
            result = add_crew(name, age)  
            if result is True:
                messagebox.showinfo("Success", "Crew added successfully!")
                add_crew_window.destroy() 
            else:
                messagebox.showerror("Error", result)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add", command=perform_add_crew).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=add_crew_window.destroy).pack(side=tk.RIGHT, padx=5)
    def cancel_flight(self):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Flight")
        cancel_window.geometry("500x400")
        main_frame = ttk.Frame(cancel_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        flights = get_all_flights()
        if not flights:
            messagebox.showinfo("No Flights", "No flights available to cancel.")
            cancel_window.destroy()
            return
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,columns=("id", "source", "dest", "date"),
                           show="headings",selectmode="browse")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.pack(fill=tk.BOTH, expand=True)
        for flight in flights:
            tree.insert("", tk.END, values=(flight[0], flight[1], flight[2], flight[3]))
        def perform_cancellation():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a flight from the list!")
                return
            flight_id = tree.item(selected_item)['values'][0]
            success, error_message = cancel_flight(flight_id)
            if success:
                messagebox.showinfo("Success", f"Flight {flight_id} cancelled successfully!")
                cancel_window.destroy()
            else:
                messagebox.showerror("Error", f"Failed to cancel flight: {error_message}")
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cancel Selected Flight", command=perform_cancellation,style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=cancel_window.destroy).pack(side=tk.RIGHT, padx=5)
    def remove_crew(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Crew Member")
        remove_window.geometry("700x500")
        main_frame = ttk.Frame(remove_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        crew_members = get_all_crew()
        if not crew_members:
            messagebox.showinfo("No Crew", "No crew members available to remove.")
            remove_window.destroy()
            return
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,columns=("id", "name", "flight_id", "age"),
                           show="headings",selectmode="browse")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("age", text="Age")
        tree.heading("flight_id", text="Flight ID")
        tree.column("id", width=50)
        tree.column("name", width=150)
        tree.column("flight_id", width=50)
        tree.column("age", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        for crew in crew_members:
            tree.insert("", tk.END, values=(crew[0], crew[1], crew[2], crew[3] or "None"))
        def perform_removal():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a crew member to remove!")
                return
            crew_id = tree.item(selected_item)['values'][0]            
            result = remove_crew(crew_id)
            if result is True:
                messagebox.showinfo("Success", "Crew member removed successfully!")
                remove_window.destroy()
            else:
                messagebox.showerror("Error", result)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Remove Selected Crew", 
                  command=perform_removal,style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=remove_window.destroy).pack(side=tk.RIGHT, padx=5)
    def remove_pilots(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Pilot")
        remove_window.geometry("700x500")
        main_frame = ttk.Frame(remove_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        pilots = get_all_pilots()
        if not pilots:
            messagebox.showinfo("No Pilots", "No pilots available to remove.")
            remove_window.destroy()
            return
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,columns=("id", "name", "age", "flight_id"),
                           show="headings",selectmode="browse")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("age", text="Age")
        tree.heading("flight_id", text="Flight ID")
        tree.column("id", width=50)
        tree.column("name", width=150)
        tree.column("age", width=50)
        tree.column("flight_id", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        for pilot in pilots:
            tree.insert("", tk.END, values=(pilot[0], pilot[1], pilot[2], pilot[3] or "None"))
        def perform_removal():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a pilot to remove!")
                return
            pilot_id = tree.item(selected_item)['values'][0]
            result = remove_pilot(pilot_id)
            if result is True:
                messagebox.showinfo("Success", "Pilot removed successfully!")
                remove_window.destroy()
            else:
                messagebox.showerror("Error", result)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Remove Selected Pilot", 
                  command=perform_removal,style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame,text="Close", command=remove_window.destroy).pack(side=tk.RIGHT, padx=5)
    def view_pilots(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("All Pilots")
        view_window.geometry("800x500")
        main_frame = ttk.Frame(view_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        pilots = view_pilots()
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                           columns=("id", "name", "age", "flight_id"),show="headings")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("age", text="Age")
        tree.heading("flight_id", text="Flight ID")
        tree.column("id", width=50)
        tree.column("name", width=150)
        tree.column("age", width=50)
        tree.column("flight_id", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        if pilots:
            for pilot in pilots:
                tree.insert("", tk.END, values=(pilot[0], pilot[1], pilot[2], pilot[3] or "Not assigned"))
        else:
            tree.insert("", tk.END, values=("No pilots found in the system", "", "", ""))
    def view_crew(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("All Crew Members")
        view_window.geometry("800x500")
        main_frame = ttk.Frame(view_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        crew_members = view_crew()
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,columns=("id", "name", "flight_id", "age"),show="headings")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("age", text="Age")
        tree.heading("flight_id", text="Flight ID")
        tree.column("id", width=50)
        tree.column("name", width=150)
        tree.column("age", width=50)
        tree.column("flight_id", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        if crew_members:
            for crew in crew_members:
                tree.insert("", tk.END, values=(crew[0], crew[1], crew[2], crew[3] or "Not assigned"))
        else:
            tree.insert("", tk.END, values=("No crew members found in the system", "", "", ""))
    def search_flights(self, customer_id=None):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Flights")
        search_window.geometry("800x600")
        main_frame = ttk.Frame(search_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        criteria_frame = ttk.LabelFrame(main_frame, text="Search Criteria", padding=10)
        criteria_frame.pack(fill=tk.X, pady=10)
        loc_frame = ttk.Frame(criteria_frame)
        loc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(loc_frame, text="From:").grid(row=0, column=0, sticky=tk.W)
        from_entry = ttk.Entry(loc_frame)
        from_entry.grid(row=1, column=0, padx=5, sticky=tk.W+tk.E)
        ttk.Label(loc_frame, text="To:").grid(row=0, column=1, sticky=tk.W)
        to_entry = ttk.Entry(loc_frame)
        to_entry.grid(row=1, column=1, padx=5, sticky=tk.W+tk.E)
        date_frame = ttk.Frame(criteria_frame)
        date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(date_frame, text="Departure Date:").grid(row=0, column=0, sticky=tk.W)
        cal = Calendar(date_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.grid(row=1, column=0, padx=5, sticky=tk.W)
        results_frame = ttk.LabelFrame(main_frame, text="Flight Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                columns=("id", "source", "dest", "date", "departure", "arrival", "price"),show="headings")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.heading("departure", text="Departure")
        tree.heading("arrival", text="Arrival")
        tree.heading("price", text="Price")
        tree.column("id", width=80)
        tree.column("source", width=100)
        tree.column("dest", width=100)
        tree.column("date", width=100)
        tree.column("departure", width=100)
        tree.column("arrival", width=100)
        tree.column("price", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
    def perform_search(self, customer_id):
        source = self.from_city.get().strip()
        destination = self.to_city.get().strip()
        trip_type = self.trip_type.get()
        if not (source and destination):
            messagebox.showerror("Error", "Please enter both source and destination!")
            return
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)
        try:
            if trip_type == "ONE WAY":
                flights = search_flights(source, destination)
                self.display_flights(flights, one_way=True)
            elif trip_type == "ROUND TRIP":
                outbound_flights = search_flights(source, destination)
                return_flights = search_flights(destination, source)
                self.display_flights(outbound_flights, return_flights)
            elif trip_type == "MULTI CITY":
                messagebox.showinfo("Info", "Please specify additional cities in the multi-city form")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    def display_flights(self, outbound_flights, return_flights=None, one_way=False):
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)
        if outbound_flights:
            for flight in outbound_flights:
                self.flights_tree.insert("", tk.END, values=(flight[0], flight[1], flight[2], flight[3], 
                flight[4], flight[5],f"₹{flight[6]}" if flight[6] else "N/A", f"₹{flight[7]}" if flight[7] else "N/A", "Outbound"))
        if return_flights and not one_way:
            for flight in return_flights:
                self.flights_tree.insert("", tk.END, 
                    values=(flight[0], flight[1], flight[2], flight[3], 
                        flight[4], flight[5], f"₹{flight[6]}" if flight[6] else "N/A", 
                        f"₹{flight[7]}" if flight[7] else "N/A", "Return"))
        if not outbound_flights and (not return_flights or one_way):
            self.flights_tree.insert("", tk.END, values=("No flights found", "", "", "", "", "", "", ""))
        if hasattr(self, 'book_btn'):
            self.book_btn.config(state=tk.NORMAL if outbound_flights else tk.DISABLED)
    def add_multi_city_leg(self, parent_frame):
        leg_frame = ttk.Frame(parent_frame)
        leg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(leg_frame, text="From:").grid(row=0, column=0, padx=5)
        from_entry = ttk.Combobox(leg_frame, values=["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai","Kolkata", "Ahmedabad", "Pune", "Jaipur", "Lucknow"])
        from_entry.grid(row=0, column=1, padx=5)
        ttk.Label(leg_frame, text="To:").grid(row=0, column=2, padx=5)
        to_entry = ttk.Combobox(leg_frame, values=["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai","Kolkata", "Ahmedabad", "Pune", "Jaipur", "Lucknow"])
        to_entry.grid(row=0, column=3, padx=5)
        ttk.Label(leg_frame, text="Date:").grid(row=0, column=4, padx=5)
        date_entry = Calendar(leg_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        date_entry.grid(row=0, column=5, padx=5)
        self.multi_city_legs.append({'from_entry': from_entry,
            'to_entry': to_entry,'date_entry': date_entry,'frame': leg_frame})
    def search_multi_city_flights(self):
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)
        try:
            all_flights = []
            for leg in self.multi_city_legs:
                source = leg['from_entry'].get().strip()
                destination = leg['to_entry'].get().strip()
                date = leg['date_entry'].get_date()
                if not (source and destination):
                    messagebox.showerror("Error", "Please fill all fields for each leg!")
                    return
                flights = search_flights(source, destination)
                if flights:
                    for flight in flights:
                        all_flights.append({'flight': flight,
                            'type': f"Leg {self.multi_city_legs.index(leg) + 1}"})
            if all_flights:
                for flight_info in all_flights:
                    flight = flight_info['flight']
                    self.flights_tree.insert("", tk.END, 
                        values=(flight[0], flight[1], flight[2], flight[3], 
                            flight[4], flight[5], f"₹{flight[6]}" if flight[6] else "N/A", 
                            f"₹{flight[7]}" if flight[7] else "N/A", flight_info['type']))
                if hasattr(self, 'book_btn'):
                    self.book_btn.config(state=tk.NORMAL)
            else:
                self.flights_tree.insert("", tk.END, values=("No flights found", "", "", "", "", "", "", ""))
                if hasattr(self, 'book_btn'):
                    self.book_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    def view_bookings(self, customer_id):
        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("My Bookings")
        bookings_window.geometry("800x500")
        main_frame = ttk.Frame(bookings_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame,yscrollcommand=scrollbar.set,
                columns=("id", "name", "flight_id", "source", "dest", "date", "seat", "class"),show="headings")
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Booking ID")
        tree.heading("name", text="Name")
        tree.heading("flight_id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.heading("seat", text="Seat")
        tree.heading("class", text="Class")
        tree.column("id", width=80)
        tree.column("name", width=80)
        tree.column("flight_id", width=80)
        tree.column("source", width=100)
        tree.column("dest", width=100)
        tree.column("date", width=100)
        tree.column("seat", width=80)
        tree.column("class", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT b.id, b.passenger_name, b.flight_id, f.source, f.destination, 
                   f.departure_date, b.seat_id, b.seat_class FROM bookings b
            JOIN flights f ON b.flight_id = f.id WHERE b.customer_id = %s""", (customer_id,))
            bookings = cursor.fetchall()
            if bookings:
                for booking in bookings:
                        tree.insert("", tk.END, values=(booking[0], booking[1], booking[2], booking[3],
                        booking[4], booking[5], booking[6], booking[7]))
            else:
                tree.insert("", tk.END, values=("No bookings found", "", "", "", "", "", "", ""))
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        def generate_pdf_ticket():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a booking first!")
                return
            booking_id = tree.item(selected_item)['values'][0]
            self.generate_ticket_pdf_by_booking(booking_id)
        ttk.Button(button_frame, text="Generate PDF Ticket", 
                  command=generate_pdf_ticket,style='TButton').pack(side=tk.LEFT, padx=5)
        def cancel_booking():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a booking first!")
                return
            booking_id = tree.item(selected_item)['values'][0]
            result = cancel_ticket(booking_id)
            if result is True:
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                bookings_window.destroy()
            else:
                messagebox.showerror("Error", result)
        ttk.Button(button_frame, text="Cancel Booking", 
                  command=cancel_booking,style='TButton').pack(side=tk.LEFT, padx=5)
    def generate_ticket_pdf(self, customer_id, flight_id, seat_id, seat_class):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT email FROM customer WHERE id = %s", (customer_id,))
            customer_email = cursor.fetchone()[0]
            cursor.execute("""SELECT source, destination, departure_date FROM flights WHERE id = %s""", (flight_id,))
            flight = cursor.fetchone()
            if not flight:
                messagebox.showerror("Error", "Flight not found!")
                return source, destination, departure_date = flight
            pdf = FPDF()
            pdf.add_page()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate ticket: {str(e)}")
        finally:
            conn.close()
     def generate_ticket_pdf_by_booking(self, booking_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT  b.passenger_name, f.source, f.destination, 
            f.departure_date, f.departure_time, f.arrival_time, b.seat_id, b.seat_class, b.id
            FROM bookings b JOIN flights f ON b.flight_id = f.id JOIN customer c ON b.customer_id = c.id WHERE b.id = %s """, (booking_id,))
            booking = cursor.fetchone()
            if not booking:
                messagebox.showerror("Error", "Booking not found!")
                return (passenger_name, source, destination, departure_date,
            departure_time, arrival_time, seat_number, seat_class, booking_id) = booking
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Celestia Airlines - E-Ticket", 0, 1, 'C')
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"Passenger: {passenger_name}", 0, 1)
            pdf.cell(0, 10, f"Flight: {source} to {destination}", 0, 1)
            pdf.cell(0, 10, f"Date: {departure_date}", 0, 1)
            pdf.cell(0, 10, f"Time: {departure_time} - {arrival_time}", 0, 1)
            pdf.ln(5)
            pdf.cell(0, 10, f"Seat: {seat_number} ({seat_class})", 0, 1)
            pdf.cell(0, 10, f"Booking ID: {booking_id}", 0, 1)
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 10, "Thank you for choosing Celestia Airlines!", 0, 1, 'C')
            filename = f"tickets/ticket_booking_{booking_id}.pdf"
            pdf.output(filename)
            messagebox.showinfo("Success", f"Ticket saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate ticket: {str(e)}")
        finally:
            conn.close()
    def cancel_ticket(self, customer_id):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Ticket")
        cancel_window.geometry("600x500")
        main_frame = ttk.Frame(cancel_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,show="headings",selectmode="browse",
                columns=("id", "flight_id", "source", "dest", "date", "seat", "class"))
        scrollbar.config(command=tree.yview)
        tree.heading("id", text="Booking ID")
        tree.heading("name", text="Passenger Name")
        tree.heading("flight_id", text="Flight ID")
        tree.heading("source", text="From")
        tree.heading("dest", text="To")
        tree.heading("date", text="Date")
        tree.heading("seat", text="Seat")
        tree.heading("class", text="Class")
        tree.column("id", width=80)
        tree.column("name" , width=80)
        tree.column("flight_id", width=80)
        tree.column("source", width=100)
        tree.column("dest", width=100)
        tree.column("date", width=100)
        tree.column("seat", width=80)
        tree.column("class", width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT b.id, b.flight_id, f.source, f.destination, 
                f.departure_date, b.seat_id, b.seat_class FROM bookings b
                JOIN flights f ON b.flight_id = f.id WHERE b.customer_id = %s""", (customer_id,))
            bookings = cursor.fetchall()
            if bookings:
                for booking in bookings:
                    tree.insert("", tk.END, values=(booking[0], booking[1], booking[2], 
                          booking[3],  booking[4], booking[5], booking[6]))
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        finally:
            conn.close()
        def perform_cancellation():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a booking to cancel!")
                return  booking_id = tree.item(selected_item)['values'][0]
            result = cancel_ticket(booking_id)
            if result is True:
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                cancel_window.destroy()
            else:
                messagebox.showerror("Error", result)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Cancel Selected Ticket",command=perform_cancellation,style='TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=cancel_window.destroy).pack(side=tk.RIGHT, padx=5)
    def book_selected_flight(self, customer_id):
        selected_items = self.flights_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one flight!")
            return
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Book Flight")
        booking_window.geometry("600x400")
        flight_info_frame = ttk.Frame(booking_window)
        flight_info_frame.pack(pady=10)
        flight_id = self.flights_tree.item(selected_items[0])['values'][0]
        source = self.flights_tree.item(selected_items[0])['values'][1]
        destination = self.flights_tree.item(selected_items[0])['values'][2]
        date = self.flights_tree.item(selected_items[0])['values'][3]
        ttk.Label(flight_info_frame, text=f"Flight {flight_id}: {source} to {destination} on {date}").pack()
        class_frame = ttk.LabelFrame(booking_window, text="Class Selection")
        class_frame.pack(pady=10)
        seat_class_var = tk.StringVar(value="economy")
        ttk.Radiobutton(class_frame, text="Economy", variable=seat_class_var, value="economy").pack(anchor=tk.W)
        ttk.Radiobutton(class_frame, text="Business", variable=seat_class_var, value="business").pack(anchor=tk.W)
        ttk.Radiobutton(class_frame, text="First Class", variable=seat_class_var, value="first_class").pack(anchor=tk.W)
        details_frame = ttk.LabelFrame(booking_window, text="Passenger Details")
        details_frame.pack(pady=10)
        ttk.Label(details_frame, text="Passenger Name:").pack()
        name_entry = ttk.Entry(details_frame)
        name_entry.pack()
        ttk.Label(booking_window, text="Seat Number:").pack()
        seat_entry = ttk.Entry(booking_window)
        seat_entry.pack()
         def perform_booking():
            seat_id = seat_entry.get()
            seat_class = seat_class_var.get()
            passenger_name = name_entry.get()
            if not all([seat_id, passenger_name]):
                messagebox.showerror("Error", "Please fill all fields!")
                return result = book_ticket(customer_id,flight_id,seat_id,
                    seat_class,passenger_name,id)
            if result is True:
                messagebox.showinfo("Success", "Booking successful!")
                booking_window.destroy()
                self.view_bookings(customer_id)  # Refresh bookings view
            else:
                messagebox.showerror("Error", result)
        ttk.Button(booking_window, text="Confirm Booking", command=perform_booking).pack(pady=10)
     def show_seats_for_booking(self, parent_frame, customer_id):
        for widget in self.seat_grid_frame.winfo_children():
            widget.destroy()
        try:
            flight_id = int(self.book_flight_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Flight ID! Must be a number")
            return 
        if not flight_exists(flight_id):
            messagebox.showerror("Error", "Flight ID does not exist!")
            return
        try:
            booked_seats = get_booked_seats(flight_id)
            self.seat_buttons = {}  # Dictionary to store seat buttons
            header_frame = ttk.Frame(self.seat_grid_frame)
            header_frame.grid(row=0, column=0, columnspan=7, sticky='ew')
            for col in range(6):
                ttk.Label(header_frame, text=str(col+1)).grid(row=0, column=col+1, padx=5)
            for row_idx in range(7):  # Rows A-G
                row_label = ttk.Label(self.seat_grid_frame, text=chr(65 + row_idx))
                row_label.grid(row=row_idx + 1, column=0, padx=5, pady=5)
                for col_idx in range(6):
                    seat = f"{chr(65 + row_idx)}{col_idx + 1}"
                    is_booked = seat in booked_seats
                    btn = tk.Button(self.seat_grid_frame,text=seat,command=lambda s=seat: self.select_seat(s),
                        width=4,state='disabled' if is_booked else 'normal',
                        bg='#ff9999' if is_booked else '#99ff99',fg='black',relief='raised')
                    btn.grid(row=row_idx + 1, column=col_idx + 1, padx=5, pady=5)
                    self.seat_buttons[seat] = btn  # Store button reference
            self.seat_grid_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.current_selected_seat = None  # Track currently selected seat
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load seats: {str(e)}")
     def select_seat(self, seat):
        if self.current_selected_seat and self.current_selected_seat in self.seat_buttons:
            btn = self.seat_buttons[self.current_selected_seat]
            if btn['state'] == 'normal':  # Only reset available seats
                btn.config(bg='#99ff99')  # Reset to green
        if seat in self.seat_buttons:
            btn = self.seat_buttons[seat]
            if btn['state'] == 'normal':  # Only allow selection of available seats
                btn.config(bg='#9999ff')  # Blue for selected
                self.current_selected_seat = seat
                self.selected_seat.set(seat)  # Update the selected seat variable
            else:
                self.current_selected_seat = None
                self.selected_seat.set("")
     def perform_booking_from_tab(self, customer_id):
        try:
            flight_id = int(self.book_flight_entry.get())
            if not flight_exists(flight_id):
                messagebox.showerror("Error", "Flight ID does not exist!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Flight ID")
            return
        seat_class = self.class_var.get()
        seat_id = self.selected_seat.get()
        passenger_name = self.name_entry.get().strip()
        if not passenger_name:
            messagebox.showerror("Error", "Please enter passenger name")
            return
        if not seat_id:
            messagebox.showerror("Error", "Please select a seat")
            return
        result = book_ticket(customer_id=customer_id,flight_id=flight_id,
            seat_id=seat_id,seat_class=seat_class,passenger_name=passenger_name)
        if result is True:
            messagebox.showinfo("Success", f"Seat {seat_id} ({seat_class}) booked successfully!")
            booking_id = self.get_last_booking_id(customer_id)
            if booking_id:
                self.generate_ticket_pdf_by_booking(booking_id)
            self.selected_seat.set("")
            self.name_entry.delete(0, tk.END)
            self.show_seats_for_booking(None, customer_id)
             self.view_bookings(customer_id)
        else:
            messagebox.showerror("Error", result)
    def get_last_booking_id(self, customer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT id FROM bookings WHERE customer_id = %s ORDER BY id DESC LIMIT 1""", (customer_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting last booking ID: {e}")
            return None
        finally:
            conn.close()
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    app = CelestiaAirlinesApp()
    app.run()