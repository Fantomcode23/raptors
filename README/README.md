# Quick Bytes
# Restaurant Management System

Quick Bytes is a web-based restaurant management system built using Flask, catering to both customers and hoteliers. It allows customers to view available hotels, menus, place orders securely, and complete payment transactions. Hoteliers can manage customer details, orders, verify OTPs, and serve food to authenticated customers.

## Table of Contents

- [Introduction](#introduction)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Installation](#installation)


## Introduction

Quick Bytes is a Flask-based restaurant management system designed to streamline the process of ordering and serving food. It offers a convenient platform for both customers and hoteliers to interact and manage their tasks efficiently.

## Tech Stack

- HTML<a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> 
- CSS<a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a>
- JavaScript
- Python <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
- Flask<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>
- SQLite <a href="https://www.sqlite.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> </a>




## Customer Interface

- View available hotels and menus.
- Select items and place orders securely.
- Complete payment transactions.
- Authenticate OTP at the hotel to receive food.

## Hotelier Interface

- Tabular view of customer details, order details, Order ID, and time (ETA of customer).
- Access customer receipts and contact details.
- Verify OTP to ensure order authenticity.
- Serve food to authenticated customers.

## Home page
![Alt text](file_2024-05-17_02.00.19.png)
## Registration page
![Alt text](file_2024-05-17_02.01.12.png)
## Sign Up page
![Alt text](file_2024-05-17_02.01.48.png)
## Restaurants page 
![Alt text](file_2024-05-17_02.02.35.png)
## Menu Page 
![Alt text](file_2024-05-17_02.03.01.png)
## Carts Page 
![Alt text](file_2024-05-17_02.03.21.png)
## Time-Slot Page 
![Alt text](file_2024-05-17_02.03.51.png)
## Payment Gateway 
![Alt text](file_2024-05-17_02.05.03.png)
## Order-Confirmation Page
![Alt text](file_2024-05-17_02.05.55.png)
## Hotelier Page
![Alt text](file_2024-05-17_02.06.34.png)



## Challenges Faced
- Integrating databases and backend with the UI
- Implementing SMTP application
    

## Installation

First, clone this repository and create a virtual environment using:
```
python -m venv venv
```
Activate the virtual environment:
```
./venv/Scripts/activate
```
Install the required packages using:
```
pip install -r requirements.txt
```
Install the SQL packages using:
```
pip install -U Flask-SQLAlchemy
```

Run the command in terminal
```
python run.py
```
Copy `http://127.0.0.1:5000/` and paste it in the address bar of a browser.


## Further Improvements
- Improving database integration
- Building better authorization service

## Team
## [S Sujeeth Shingade](https://github.com/sujeethshingade)
## [Mayank Chaturvedi](https://github.com/mayankch283)
## [Sujay J Ram](https://github.com/SujJR)
## [Ankit A K](https://github.com/Ankman07)









