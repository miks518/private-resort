# Jaime Place Private Resort System

A comprehensive, full-stack resort booking and management system built with Django. This application handles everything from customer reservations and dynamic facility showcasing to automated email notifications and secure online payments.

## ✨ Key Features

* **Modern Dark Mode UI:** Features a custom "Deep Ocean" dark mode design aesthetic using pure CSS, glassmorphism, and responsive bento grid galleries.
* **Online Reservations:** A robust booking engine that prevents double-booking and handles maximum capacity checks.
* **Automated Payments:** Fully integrated with the **PayMongo** API (supporting GCash, Maya, and Cards) including webhook handling for real-time payment confirmation.
* **Email Notifications:** Built-in SMTP support that automatically dispatches booking and payment receipts directly to the resort admin.
* **Admin Dashboard:** A secured Django admin panel for managing facilities, updating pricing, checking reservations, and monitoring transaction statuses.

## 🛠️ Technology Stack

* **Backend:** Python + Django
* **Frontend:** HTML5, Vanilla CSS3 (Custom Design System), JavaScript
* **Database:** SQLite (Local/Dev) / PostgreSQL (Production ready)
* **Media Storage:** Cloudinary integration for handling high-quality gallery images
* **APIs:** PayMongo (Payments), Google SMTP (Email)

## 🚀 Getting Started Locally

Follow these instructions to run the website on your local Windows/Mac machine.

### 1. Prerequisites
Ensure you have the following installed:
* [Python 3.12+](https://www.python.org/downloads/)
* Git

### 2. Clone the Repository
```bash
git clone https://github.com/miks518/private-resort.git
cd private-resort
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```
Activate the environment:
* On **Windows**: `.\venv\Scripts\activate`
* On **Mac/Linux**: `source venv/bin/activate`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create a `.env` file in the root directory (same level as `manage.py`) and grab the required keys:
```env
DEBUG=True
SECRET_KEY=local-secret-key-for-dev
DATABASE_URL= # Leave blank for local SQLite

# Live Payment Processing (PayMongo)
PAYMONGO_PUBLIC_KEY=pk_test_...
PAYMONGO_SECRET_KEY=sk_test_...

# Email Automation (Gmail)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
```

### 6. Run Migrations & Start the Server
Apply database migrations to setup the schema:
```bash
python manage.py migrate
```

Start the local development server:
```bash
python manage.py runserver
```
The raw website is now active! Visit `http://127.0.0.1:8000` in your web browser.

### 7. Access the Admin Panel
To create facilities and view reservations, create an admin account:
```bash
python manage.py createsuperuser
```
Log in at `http://127.0.0.1:8000/admin/`.
