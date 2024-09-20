# Rental Management System

## Description

The **Rental Management System** is a Command-Line Interface (CLI) application that allows property managers and landlords to efficiently manage their rental properties. The system enables users to handle various tasks such as managing properties, tenants, and payments, as well as generating reports and updating property statuses. This system is built using Python and PostgreSQL.

## Features

1. **Property Management**: Add, view, update, and delete properties.
2. **Tenant Management**: Add tenants and view tenant information, including linked property addresses.
3. **Payment Tracking**: Add rental payments and view payments, including tenant names and property addresses.
4. **Update Property Status**: Change the status of properties (e.g., available, rented, under maintenance).
5. **Delete Properties**: Delete properties and manage dependencies (tenants and payments).

## Technologies Used

- **Python**: Core programming language.
- **PostgreSQL**: Database for storing property, tenant, and payment information.
- **Psycopg2**: PostgreSQL adapter for Python.
- **CLI**: Command-line interface for user interaction.

## Installation

### Prerequisites

- Python 3.x installed
- PostgreSQL installed and running
- Pipenv for managing the virtual environment

### Steps to Install

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/rental-management-system.git
    cd rental-management-system
    ```

2. Set up the virtual environment:

    ```bash
    pipenv install
    ```

3. Install required dependencies:

    ```bash
    pipenv install psycopg2-binary
    ```

4. Create a PostgreSQL database for the project:

    ```sql
    CREATE DATABASE rental_management;
    ```

5. Set up your PostgreSQL credentials in the `create_connection()` function within the code (update the `dbname`, `user`, `password`, and `host`).

6. Run the application:

    ```bash
    pipenv run python models.py
    ```

## How to Use

Once the system is running, you will be presented with a menu for managing properties, tenants, and payments. Here’s how to use each option:

### Menu Options

1. **Add Property**: Allows you to add a new property to the system by providing details like location and type.
2. **View Properties**: Displays all the properties along with their details (address, type, status).
3. **Add Tenant**: Enables you to add a tenant to a specific property by entering their name and contact details.
4. **View Tenants**: Displays a list of tenants, including their associated property addresses.
5. **Add Payment**: Records a rental payment, including tenant name and payment amount.
6. **View Payments**: Displays a list of payments, showing the tenant name and the apartment they are renting.
7. **Update Property Status**: Allows you to change the status of a property (e.g., rented, available, under maintenance).
8. **Delete Property**: Deletes a property and all related tenants and payments from the database.
9. **Exit**: Exit the system.

### Example Usage

```plaintext
Rental Management System
1. Add Property
2. View Properties
3. Add Tenant
4. View Tenants
5. Add Payment
6. View Payments
7. Update Property Status
8. Delete Property
9. Exit
Enter choice: 1
Enter property location: 123 Main St
Enter property type (e.g., apartment, house): apartment
Property added successfully!
