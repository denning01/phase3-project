import psycopg2

# Database connection setup
def create_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="rental_management",
        user="denning",  # Replace with your PostgreSQL username
        password="1234"  # Replace with your PostgreSQL password
    )
    return connection

# Create Tables
def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # Property Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
            address VARCHAR(255) NOT NULL,
            property_type VARCHAR(50),
            status VARCHAR(50) DEFAULT 'vacant'
        );
    ''')

    # Tenant Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact VARCHAR(100),
            property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL
        );
    ''')

    # Payment Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            tenant_id INTEGER REFERENCES tenants(id) ON DELETE SET NULL
        );
    ''')

    connection.commit()
    cursor.close()
    connection.close()
    print("Tables created successfully!")

# Add a property
def add_property(address, property_type, status='vacant'):
    connection = create_connection()
    cursor = connection.cursor()
    
    insert_query = '''
        INSERT INTO properties (address, property_type, status) 
        VALUES (%s, %s, %s) RETURNING id;
    '''
    cursor.execute(insert_query, (address, property_type, status))
    property_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Property with id {property_id} added!")
    return property_id

# Add a tenant
def add_tenant(name, contact, property_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    insert_query = '''
        INSERT INTO tenants (name, contact, property_id) 
        VALUES (%s, %s, %s) RETURNING id;
    '''
    cursor.execute(insert_query, (name, contact, property_id))
    tenant_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Tenant with id {tenant_id} added!")
    return tenant_id

# Add a payment
def add_payment(amount, date, tenant_id):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = '''
        INSERT INTO payments (amount, date, tenant_id) 
        VALUES (%s, %s, %s) RETURNING id;
    '''
    cursor.execute(insert_query, (amount, date, tenant_id))
    payment_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Payment with id {payment_id} added!")
    return payment_id

# View all properties
def get_properties():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = '''
        SELECT * FROM properties;
    '''
    cursor.execute(select_query)
    properties = cursor.fetchall()

    cursor.close()
    connection.close()
    return properties

# View all tenants
def get_tenants():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = '''
        SELECT tenants.id, tenants.name, tenants.contact, properties.address
        FROM tenants
        LEFT JOIN properties ON tenants.property_id = properties.id;
    '''
    cursor.execute(select_query)
    tenants = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Return tenants with property addresses
    return tenants

# View all payments
# View all payments with tenant names and property addresses
def get_payments():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = '''
        SELECT payments.id, payments.amount, payments.date, tenants.name, properties.address
        FROM payments
        JOIN tenants ON payments.tenant_id = tenants.id
        LEFT JOIN properties ON tenants.property_id = properties.id;
    '''
    cursor.execute(select_query)
    payments = cursor.fetchall()

    cursor.close()
    connection.close()

    # Return payments with tenant names and property addresses
    return payments

# Update property status
def update_property_status(property_id, new_status):
    connection = create_connection()
    cursor = connection.cursor()

    update_query = '''
        UPDATE properties 
        SET status = %s 
        WHERE id = %s;
    '''
    cursor.execute(update_query, (new_status, property_id))

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Property {property_id} status updated to {new_status}!")

# Delete a property
# Delete tenants associated with the property
# Delete payments associated with the tenant
def delete_payments_by_tenant_id(tenant_id):
    connection = create_connection()
    cursor = connection.cursor()

    delete_payments_query = '''
        DELETE FROM payments WHERE tenant_id = %s;
    '''
    cursor.execute(delete_payments_query, (tenant_id,))
    connection.commit()

    cursor.close()
    connection.close()

# Delete tenants associated with the property
def delete_tenants_by_property_id(property_id):
    connection = create_connection()
    cursor = connection.cursor()

    # First, retrieve tenants associated with this property
    select_tenants_query = '''
        SELECT id FROM tenants WHERE property_id = %s;
    '''
    cursor.execute(select_tenants_query, (property_id,))
    tenants = cursor.fetchall()

    # For each tenant, delete their payments
    for tenant in tenants:
        tenant_id = tenant[0]
        delete_payments_by_tenant_id(tenant_id)

    # Now, delete the tenants
    delete_tenants_query = '''
        DELETE FROM tenants WHERE property_id = %s;
    '''
    cursor.execute(delete_tenants_query, (property_id,))
    connection.commit()

    cursor.close()
    connection.close()

# Delete property by ID
def delete_property(property_id):
    # First, delete tenants associated with this property (and their payments)
    delete_tenants_by_property_id(property_id)

    # Now, delete the property
    connection = create_connection()
    cursor = connection.cursor()

    delete_query = '''
        DELETE FROM properties WHERE id = %s;
    '''
    cursor.execute(delete_query, (property_id,))
    connection.commit()

    cursor.close()
    connection.close()

    print(f"Property with ID {property_id} has been deleted.")


# Menu
def menu():
    print("\nRental Management System")
    print("1. Add Property")
    print("2. View Properties")
    print("3. Add Tenant")
    print("4. View Tenants")
    print("5. Add Payment")
    print("6. View Payments")
    print("7. Update Property Status")
    print("8. Delete Property")
    print("9. Exit")

# Main program
def main():
    create_tables()  # Ensure tables are created before using the system
    
    while True:
        menu()
        choice = input("Enter choice: ")
        
        if choice == '1':
            address = input("Enter property address: ")
            property_type = input("Enter property type (apartment/house): ")
            add_property(address, property_type)
        
        elif choice == '2':
            properties = get_properties()
            for p in properties:
                print(p)

        elif choice == '3':
            name = input("Enter tenant name: ")
            contact = input("Enter tenant contact: ")
            property_id = input("Enter property id: ")
            add_tenant(name, contact, property_id)

        elif choice == '4':
            tenants = get_tenants()
            for t in tenants:
                print(t)

        elif choice == '5':
            amount = input("Enter payment amount: ")
            date = input("Enter payment date (YYYY-MM-DD): ")
            tenant_id = input("Enter tenant id: ")
            add_payment(amount, date, tenant_id)

        elif choice == '6':
            payments = get_payments()
            for p in payments:
                print(p)

        elif choice == '7':
            property_id = input("Enter property id: ")
            status = input("Enter new status (vacant/occupied): ")
            update_property_status(property_id, status)

        elif choice == '8':
            property_id = input("Enter property id to delete: ")
            delete_property(property_id)

        elif choice == '9':
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
