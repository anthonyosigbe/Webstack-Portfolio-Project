# Webstack - Portfolio Project

# Group project Front-end Back-end Portfolio project<

# ThroneHub Financial Manager

## Project Description
ThroneHub Financial Manager is designed to help users track their expenses, manage budgets, and analyze their financial health. The application provides a user-friendly interface for managing personal finances, offering tools for expense tracking, budget management, and financial analysis with visual data representation.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Development Highlights](#development-highlights)
- [Challenges](#challenges)
- [Next Steps](#next-steps)
- [Contributing](#contributing)
- [License](#license)

## Features
- User authentication (registration, login, password reset)
- Expense and income management
- Budget tracking
- Financial analysis with data visualization using Chart.js
- Data export in CSV and Excel formats
- Customizable Django admin interface

## Technologies Used
- **Backend:** Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **AJAX:** User registration, login, password reset
- **Data Visualization:** Chart.js
- **Additional Technologies:** JSON, CSV, Excel export

## System Architecture
The application follows a traditional web application architecture:
1. **Frontend:** User interface built with HTML, CSS, and JavaScript.
2. **Backend:** Django framework handling business logic and data processing.
3. **Database:** PostgreSQL for storing user data and financial records.
4. **AJAX:** Handling asynchronous requests for user actions.
5. **Data Visualization:** Chart.js for rendering financial data graphs.
6. **Export Functionality:** Allowing data export in CSV and Excel formats.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/anthonyosigbe/Webstack-Portfolio-Project.git

2. Change to the project directory:
   ```bash
   cd thronehubfinancialmanager

3. Create a virtual environment:
   ```bash
   pipenv 

4. Activate the virtual environment:
   ```bash
   pipenv shell

5. Install dependencies:
  ```bash
   pipenv install "dependecies/pakages"
  
6. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate


7. Create a superuser for accessing the admin interface:
   ```bash
   python manage.py createsuperuser

8. Run the development server:
   ```bash
   python manage.py runserver


## Usage

1. Open your web browser and navigate to http://localhost:8000.
2. Register a new user or log in with existing credentials.
3. Start tracking your expenses and income.
4. Visualize your financial data using the built-in charts.
5. Export your data in CSV or Excel format as needed.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to your fork and submit a pull request.





