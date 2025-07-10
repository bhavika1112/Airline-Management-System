# ✈️ Celestia Airlines – Airline Management System

An interactive airline management system built in Python to streamline flight bookings, seat reservations, and user authentication. The system offers separate interfaces for admins and customers, integrates weather safety checks via API, and ensures real-time ticketing with a MySQL backend and a GUI built with Tkinter.

---

## 🚀 Features

* **User Roles**

  * Customer registration/login
  * Admin login with full access
* **Admin Dashboard**

  * Add/update/delete flights *(Note: Known bug in "Add Flights" section – under debugging)*
  * Assign pilots/crew
  * View all customer bookings
* **Flight Search & Booking**

  * Filter by source/destination
  * Real-time seat selection with GUI
* **Ticket Management**

  * PDF ticket generation with flight and seat details
  * View, download, and cancel bookings
* **Weather Integration**

  * Live weather data using OpenWeatherMap API
* **Backend**

  * MySQL database integration (via XAMPP)
* **GUI**

  * Built with Tkinter (modular, user-friendly)

---

## 🛠️ Tech Stack

| Component            | Technology/Library          |
| -------------------- | --------------------------- |
| Programming Language | Python 3.10+                |
| GUI                  | Tkinter                     |
| Database             | MySQL via XAMPP             |
| API Integration      | OpenWeatherMap + `requests` |
| Editor               | Sublime Text 3              |

---

## 📝 Project Structure

* `customer_login.py` – Customer authentication
* `admin_dashboard.py` – Admin panel with flight/crew management
* `book_flight.py` – Flight search and booking interface
* `weather_check.py` – API integration for weather updates
* `db_config.py` – MySQL connection setup

---

## ⚠️ Known Issues

* Flight addition via admin panel may throw an error due to validation or database mismatch. This is currently being debugged.
