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
    while option != "5":
        print("\nSelect one of the following menu options:\n1. Create Account \n2. View Account \n3. Desposit \n4. Withdrawal \n5. Quit")
        option = input("Your Choice: ")

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
            if customer_data is None:
                print('There is no account under that ID.')
            else:
                # Retrieve assets and their values
                cur.execute(f"SELECT name, value FROM asset WHERE customer_id = {id}")
                assets = cur.fetchall()
    
                # Calculate the total value of assets
                cur.execute(f"SELECT SUM(value) FROM asset WHERE customer_id = {id}")
                asset_value = cur.fetchone()[0]
                # Get value of coin and assets combined
                if asset_value is None:
                    total_value = customer_data[1]
                else:
                    total_value = asset_value + customer_data[1]
    
                # Print the information
                print(f"\nName: {customer_data[0]}")
                print(f"Coin: {customer_data[1]}")
                
                if asset_value is None:
                    print(f"Assets: {asset_value}")
                else:
                    print("Assets:")
                    for asset in assets:
                        print(f"- {asset[0]}: {asset[1]}")
                print(f"Asset Value: {asset_value}")
                print(f"Total Account Value: {total_value}")

        elif option == "3":
            deposit_option = 0
            # Deposit an asset into the customer's account
            while deposit_option != "3":
                print("\nDeposit Menu:")
                print("1. Deposit Coins")
                print("2. Deposit Asset")
                print("3. Back to Main Menu")
                deposit_option = input("Select an option: ")
        
                if deposit_option == "1":
                    # Deposit coins into the customer's account
                    id = input("What is your account id? ")
                    coins_to_deposit = float(input("How many coins would you like to deposit? "))
            
                    # Retrieve the current coin balance
                    cur.execute(f"SELECT coin FROM customer WHERE customer_id = {id}")
                    current_coin_balance = cur.fetchone()[0]
            
                    # Update the coin balance
                    new_coin_balance = current_coin_balance + coins_to_deposit
                    cur.execute(f"UPDATE customer SET coin = {new_coin_balance} WHERE customer_id = {id}")
                    con.commit()
                    print(f"You have deposited {coins_to_deposit} coins. Your new coin balance is {new_coin_balance}.")
        
                elif deposit_option == "2":
                    # Deposit assets into the customer's account
                    id = input("What is your account id? ")
                    asset_name = input("Enter the name of the asset you want to deposit: ")
                    asset_value = float(input("Enter the value of the asset: "))
            
                    cur.execute("SELECT MAX(asset_id) FROM asset")
                    max_asset_id = cur.fetchone()[0]
            
                    # Check if max_asset_id is None (empty table), and set it to 0 if needed
                    if max_asset_id is None:
                       max_asset_id = 0
            
                    # Calculate the new asset_id
                    asset_id = max_asset_id + 1
            
                    # Insert the asset into the "asset" table
                    insert_query = cur.execute("INSERT INTO asset (asset_id, name, value, customer_id) VALUES (?, ?, ?, ?)", (asset_id, asset_name, asset_value, id))

        elif option == "4":
            withdrawal_option = 0
            # Withdraw an asset or coins from the customer's account
            while withdrawal_option != "3":
                print("\nWithdrawal Menu:")
                print("1. Withdraw Coins")
                print("2. Withdraw Asset")
                print("3. Back to Main Menu")
                withdrawal_option = input("Select an option: ")
        
                if withdrawal_option == "1":
                    # Withdraw coins from the customer's account
                    id = input("What is your account id? ")
                    coins_to_withdraw = float(input("How many coins would you like to withdraw? "))
            
                    # Retrieve the current coin balance
                    cur.execute(f"SELECT coin FROM customer WHERE customer_id = {id}")
                    current_coin_balance = cur.fetchone()[0]
            
                    if current_coin_balance >= coins_to_withdraw:
                        # Update the coin balance
                        new_coin_balance = current_coin_balance - coins_to_withdraw
                        cur.execute(f"UPDATE customer SET coin = {new_coin_balance} WHERE customer_id = {id}")
                        con.commit()
                        print(f"You have withdrawn {coins_to_withdraw} coins. Your new coin balance is {new_coin_balance}.")
                    else:
                        print("Insufficient coins in your account.")
        
                elif withdrawal_option == "2":
                    # Withdraw assets from the customer's account
                    id = input("What is your account id? ")
                    asset_id = input("Enter the ID of the asset you want to withdraw: ")
            
                    # Check if the asset exists and belongs to the customer
                    cur.execute(f"SELECT asset_id FROM asset WHERE asset_id = {asset_id} AND customer_id = {id}")
                    asset_exists = cur.fetchone()
            
                    if asset_exists:
                        cur.execute(f"DELETE FROM asset WHERE asset_id = {asset_id}")
                        con.commit()
                        print(f"Asset {asset_id} has been withdrawn from your account.")
                    else:
                        print(f"Asset {asset_id} does not exist in this account.")


con.commit()

# Close the cursor and the database connection
cur.close()
con.close()