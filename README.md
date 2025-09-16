# Event Booking System
A simple Flask-based Event Booking System that allows users to register, log in, view events, and book them. Organizers can also create and delete events.

# Features
- User registration and login
- User roles: attendee and organizer
- Attendees can book events
- Organizers can create and delete events
- Profile page with booking history
- SQLite database integration
- Responsive UI with Bootstrap 5

# Tech Stack
- Backend: Python (Flask)
- Frontend: HTML, Jinja2, Bootstrap 5
- Database: SQLite3

## 📂 Project Structure
event-booking-system/
│── app.py # Main Flask application
│── database.py # Database setup and helper functions
│── requirements.txt # Python dependencies
│── README.md # Project documentation
│
├── templates/ # HTML templates (Jinja2)
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── profile.html
│ └── events.html
│
├── static/ # Static files
│ ├── css/
│ │ └── style.css
│ └── images/
│ └── logo.png
│
└── booking.db # Database storage

## ⚙️ Installation & Setup
Follow these steps to set up and run the project locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/naduto/event-booking-system.git
   cd event-booking-system

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate      # On Windows

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up the database**
   ```bash
    python database.py

5. **Run the Flask application**
   ```bash
    python app.py

6. **Open the application in your browser**

   Once the server is running, open your browser and go to:

   👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## User Roles
-Attendee: Can register, login, view events, and book them.

-Organizer: Can create, delete events, and manage attendees

## Future Improvements

- Edit Event functionality for organizers

- Email notifications for bookings

- Event search & filter

- Profile picture support
