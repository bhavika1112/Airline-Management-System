import mysql.connector
from tkinter import messagebox
from fpdf import FPDF
def get_db_connection():
    try:
        conn = mysql.connector.connect(host="localhost",user="root",password="", database="celestia_airlines")
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
        return None
def get_connection_and_cursor():
    conn = get_db_connection()
    if conn:
        return conn, conn.cursor()
    else:
        return None, None
def customer_login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM customer WHERE email = %s AND password = %s", (email, password))
    customer = cursor.fetchone()
    conn.close()
    return customer
def search_flights(source, destination):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    query = """
        SELECT id, source, destination, departure_date, departure_time, arrival_time,economy_price, business_price, first_class_price
        FROM flights WHERE source LIKE %s AND destination LIKE %s"""
    cursor.execute(query, (f"%{source}%", f"%{destination}%"))
    flights = cursor.fetchall()
    conn.close()
    return flights
def get_booked_seats(flight_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("SELECT seat_id FROM bookings WHERE flight_id = %s", (flight_id,))
        booked_seats = [row[0] for row in cursor.fetchall()]
        return booked_seats
    except Exception as e:
        return str(e)
    finally:
        conn.close()
def book_ticket(customer_id, flight_id, seat_id, seat_class, passenger_name):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("SELECT id FROM flights WHERE id = %s", (flight_id,))# Check if flight exists
        if not cursor.fetchone():  # Make sure to fetch the result
            return "Flight not found"
        cursor.execute("SELECT id FROM bookings WHERE flight_id = %s AND seat_id = %s", (flight_id, seat_id))
        if cursor.fetchone():  # Make sure to fetch the result
            return "Seat already booked"
        price_column = f"{seat_class}_price"
        cursor.execute(f"SELECT {price_column} FROM flights WHERE id = %s", (flight_id,))
        price_result = cursor.fetchone()  # Make sure to fetch the result
        if not price_result:
            return "Could not determine price"
        price = price_result[0]
        cursor.execute("""INSERT INTO bookings (id, customer_id, flight_id, seat_id, seat_class, passenger_name, booking_date)
VALUES (%s, %s, %s, %s, %s, %s, CURDATE())""", (id,customer_id, flight_id, seat_id, seat_class, passenger_name))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return f"Database error: {err}"
    finally:
        conn.close()
def cancel_ticket(booking_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("SELECT customer_id, flight_id FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        if booking:
            customer_id, flight_id = booking
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
            cursor.execute("""UPDATE customer SET flight_id = NULL WHERE id = %s AND flight_id = %s
                AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customer' AND column_name = 'flight_id'
                )""", (customer_id, flight_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
def get_all_flights():
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return []
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    conn.close()
    return flights
def get_all_crew():
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return []
    cursor.execute("SELECT * FROM crew")
    crew = cursor.fetchall()
    conn.close()
    return crew
def get_all_pilots():
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return []
    cursor.execute("SELECT id, name, age, flight_id FROM pilots")
    pilots = cursor.fetchall()
    conn.close()
    return pilots
def add_pilot(name, age):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("""SELECT f.id FROM flights f LEFT JOIN pilots p ON f.id = p.flight_id GROUP BY f.id HAVING COUNT(p.id) < 2 LIMIT 1""")
        flight_result = cursor.fetchone()
        flight_id = flight_result[0] if flight_result else None
        if flight_id:
            cursor.execute("""INSERT INTO pilots (name, age, flight_id) VALUES (%s, %s, %s)""", (name, age, flight_id))
        else:
            cursor.execute("""INSERT INTO pilots (name, age, flight_id) VALUES (%s, %s, NULL)""", (name, age))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
def add_crew(name, age):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("""SELECT flights.id FROM flights LEFT JOIN crew ON flights.id = crew.flight_id
            GROUP BY flights.id HAVING COUNT(crew.id) < 4 LIMIT 1""")
        flight_result = cursor.fetchone()
        flight_id = flight_result[0] if flight_result else None
        if flight_id:
            cursor.execute("INSERT INTO crew (name, age, flight_id) VALUES (%s, %s, %s)", (name, age, flight_id))
        else:
            cursor.execute("INSERT INTO crew (name, age, flight_id) VALUES (%s, %s, NULL)", (name, age))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
def add_flight(source, destination, departure_date, departure_time, arrival_time,first_class_seats=10,
               economy_price, business_price, first_class_price,economy_seats=60, business_seats=20):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return False, "Database connection error"
    try:
        cursor.execute('''INSERT INTO flights 
        (source, destination, departure_date, departure_time, arrival_time,economy_price, business_price, first_class_price,
         economy_seats, business_seats, first_class_seats)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (source, destination, departure_date, departure_time, arrival_time,
              economy_price, business_price, first_class_price,economy_seats, business_seats, first_class_seats))
        conn.commit() 
        return True, None
    except mysql.connector.Error as err:
        conn.rollback()
        return False, f"Database error: {err}"
    finally:
        conn.close()
def cancel_flight(flight_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return False, "Database connection error"
    try:
        cursor.execute("UPDATE customer SET flight_id = NULL WHERE flight_id = %s", (flight_id,))
        cursor.execute("UPDATE crew SET flight_id = NULL WHERE flight_id = %s", (flight_id,))
        cursor.execute("UPDATE pilots SET flight_id = NULL WHERE flight_id = %s", (flight_id,))
        cursor.execute("DELETE FROM bookings WHERE flight_id = %s", (flight_id,))
        cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
def view_bookings(customer_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return []
    try:
        cursor.execute("""SELECT b.id, b.flight_id, f.source, f.destination, 
               f.departure_date, b.seat_id, b.seat_class FROM bookings b
        JOIN flights f ON b.flight_id = f.id WHERE b.customer_id = %s """, (customer_id,))
        bookings = cursor.fetchall()
        return bookings
    except Exception as e:
        return str(e)
    finally:
        conn.close()
def remove_crew(crew_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("DELETE FROM crew WHERE id = %s", (crew_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
def remove_pilot(pilot_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute("DELETE FROM pilots WHERE id = %s", (pilot_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()
def view_pilots():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, flight_id FROM pilots")
    pilots = cursor.fetchall()
    conn.close()
    return pilots
def view_crew():
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return []
    cursor.execute("SELECT id, name,flight_id, age FROM crew")
    crew = cursor.fetchall()
    conn.close()
    return crew
def flight_exists(flight_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM flights WHERE id = %s)", (flight_id,))
    exists = cursor.fetchone()[0]
    conn.close()
    return bool(exists)
def get_booking_details(booking_id):
    conn, cursor = get_connection_and_cursor()
    if not conn:
        return "Database connection error"
    try:
        cursor.execute(""" SELECT b.id, f.source, f.destination, f.departure_date, f.departure_time, f.arrival_time,
                   b.seat_id, b.seat_class FROM bookings b JOIN flights f ON b.flight_id = f.id WHERE b.id = %s""", (booking_id,))
        return cursor.fetchone()
    except Exception as e:
        return str(e)
    finally:
        conn.close()
def generate_booking_pdf(booking_id, filename):
    booking = get_booking_details(booking_id)
    if not booking or isinstance(booking, str):
        return False, booking if isinstance(booking, str) else "Booking not found"
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        labels = ["Booking ID", "Source", "Destination", "Date", "Seat ID", "Class"]
        for i, value in enumerate(booking):
            pdf.cell(200, 10, txt=f"{labels[i]}: {value}", ln=1)
        pdf.output(filename)
        return True, None
    except Exception as e:
        return False, str(e)