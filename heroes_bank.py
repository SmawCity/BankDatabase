import sqlite3

con = sqlite3.connect("bank.db")
cur = con.cursor()
con.execute("PRAGMA foreign_keys = ON;")

# Define the SQL command to create the table
create_customer_table_query = """
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    coin INTEGER
);
"""

create_asset_table_query = """
CREATE TABLE IF NOT EXISTS asset (
    asset_id INTEGER PRIMARY KEY,
    name TEXT,
    value INTEGER,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);
"""


# Execute the SQL command
# query = cur.execute("""
#     INSERT INTO customer VALUES
#         (1, 'Zym Myrett'),
#         (2, 'Suad Deeb')
# """)

# query = cur.execute("""
#     INSERT INTO asset VALUES
#         (1, 'Abracadabrus', 20000, 1),
#         (2, 'Opal', 100, 2)
# """)

cur.execute(create_customer_table_query)
cur.execute(create_asset_table_query)

# Class for the account menu
class Menu:
    print("Welcome to the Heroes' Bank!")
    option = ""
    id = 0
    while option != "Q":
        print("\nSelect one of the following menu options or type 'Q' to quit:\n1. Create Account \n2. View Account \n3. Desposit \n4. Withdrawal")
        option = input("Your Choice: ").upper()

        if option == "1":
            # Create a new account by assigning an account ID and getting the customer's name
            name = input("What is the name you want under the account? ")
            coin = input("What will your account balance be in coinage? ")
            # Retrieve the maximum customer_id
            cur.execute("SELECT MAX(customer_id) FROM customer")
            max_customer_id = cur.fetchone()[0]
            # Check if the customer table is empty, setting the max ID to 0 if needed
            if max_customer_id is None:
                max_customer_id = 0
            # Increment it by 1 to assign a new customer_id
            id = max_customer_id + 1
            insert_query = cur.execute("INSERT INTO customer (customer_id, name, coin) VALUES (?, ?, ?)",
                            (id, name, coin))
            print(f"Your account has been created! Your account ID is {id}.")
            con.commit()

        elif option == "2":
            # View the customer's account, assets, value of those assets, and the total value of all of their assets combined
            id = input("What is your account id? ")
            # Retrieve customer name and coinage
            cur.execute(f"SELECT name, coin FROM customer WHERE customer_id = {id}")
            customer_data = cur.fetchone()
    
            # Retrieve assets and their values
            cur.execute(f"SELECT name, value FROM asset WHERE customer_id = {id}")
            assets = cur.fetchall()
    
            # Calculate the total value of assets
            cur.execute(f"SELECT SUM(value) FROM asset WHERE customer_id = {id}")
            asset_value = cur.fetchone()[0]
            # Get value of coin and assets combined
            total_value = asset_value + customer_data[1]
    
            # Print the information
            print(f"\nName: {customer_data[0]}")
            print(f"Coin: {customer_data[1]}")
            print("Assets:")
            for asset in assets:
                print(f"- {asset[0]}: {asset[1]}")
            print(f"Asset Value: {asset_value}")
            print(f"Total Account Value: {total_value}")

        elif option == "3":
            # Deposit an asset into the customer's account
            id = input("What is your account id? ")
            # Retrieve the maximum asset_id
            cur.execute("SELECT MAX(asset_id) FROM asset")
            max_asset_id = cur.fetchone()[0]
    
            # Check if max_asset_id is None (empty table), and set it to 0 if needed
            if max_asset_id is None:
                max_asset_id = 0
            asset_id = max_asset_id + 1
    
            name = input("What asset would you like to deposit? ")
            value = input("What is the asset worth? ")
    
            # Use placeholders in the SQL query to safely insert values
            insert_query = cur.execute("INSERT INTO asset (asset_id, name, value, customer_id) VALUES (?, ?, ?, ?)",
                               (asset_id, name, value, id))
    
            con.commit()
            print(f"Your {name} has been deposited!")

        elif option == "4":
            # Withdraw an asset from the customer's account
            id = input("What is your account id? ")

            # Retrieve assets and their IDs and values
            cur.execute(f"SELECT asset_id, name, value FROM asset WHERE customer_id = {id}")
            assets = cur.fetchall()
    
            if not assets:
                print("No assets to withdraw.")
            else:
                print("Available Assets:")
            for asset in assets:
                print(f"ID: {asset[0]}, Name: {asset[1]}, Value: {asset[2]}")
        
            withdrawn_asset_id = input("\nEnter the ID of the asset you would like to withdraw: ")
        
            # Check if the entered ID is valid
            asset_ids = [str(asset[0]) for asset in assets]
            if withdrawn_asset_id not in asset_ids:
                print("Invalid asset ID.")
            else:
                # Delete the selected asset
                cur.execute(f"DELETE FROM asset WHERE asset_id = {withdrawn_asset_id}")
                print("Asset withdrawn successfully.")
    
            con.commit()


con.commit()

# Close the cursor and the database connection
cur.close()
con.close()