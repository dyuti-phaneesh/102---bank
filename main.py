import mysql. connector
import sys 



### LOG IN / CREATE ACCOUNT
def checkLogInNumber(num):
    
    isValid = False
    while(isValid == False):
        if num == 1:
            isValid == True
            logIn()
            break
        elif num == 2:
            isValid == True
            createAccount()
            break
        else: 
            num = int(input('\n      Please enter a valid number:\n\n'))
            checkLogInNumber(num)

def createAccount():
    print('---------create account---------')
    username = input('\nEnter a username: ')
    password = input('Enter a password: ')

    create_account_query = "INSERT INTO user_info (user_name, password) VALUES (%s, %s)"
    value = (username, password)
    cursor.execute(create_account_query, value)
    connection.commit()

    cursor.execute("SELECT * FROM user_info")
    result = cursor.fetchall()
    for row in result:
        if row[1] == username and row[2] == password:
            global userID
            userID = row[0]
    connection.commit()
    account_actions()

    ## if account already exists, ask to change info

def logIn():
    print('---------log in---------')
    username = input('\nEnter your username: ')
    password = input('Enter your password: ')

    cursor.execute("SELECT * FROM user_info")
    result = cursor.fetchall()
    for row in result:
        if row[1] != username and row[2] != password:
            print('\nYour account does not exist. Please create an account: ')
            createAccount()    
        else: 
            print(f'log in successful: Welcome {username}!')
            global userID
            userID = row[0]
            account_actions()
            break
    connection.commit()

### AFTER LOG IN, DISPLAY MENU:
def account_actions():
    action = int(input("""
    -------------------------------
       * BANK ACCOUNT ACTIONS *

           Enter a number: 
    -------------------------------
    1. Check Balance ------------->
    2. Deposit ------------------->
    3. Withdraw ------------------>
    4. Account Settings ---------->
    -------------------------------
    
    """))
    if action == 1:
        check_balance()
    if action == 2:
        deposit_money()
    if action == 3:
        withdraw_money()
    if action == 4:
        account_settings()

### BANK ACTIONS
def check_balance():
    print('--------- check balance ---------')
    
    cursor.execute("SELECT * FROM user_info")
    result = cursor.fetchall()
    for row in result:
        if row[0] == userID:
            balance = row[3]
            print('\nACCOUNT BALANCE: $' + str(balance))
            choice = input('\nWould you like to deposit money?\n')
            for i in choice:
                if i == 'y': 
                    deposit_money()
                if i == 'n' and balance > 0:
                    choice2 = input('Would you like to withdraw money?\n')
                    for i in choice2:
                        if i == 'y': 
                            withdraw_money()
                        if i == 'n':
                            account_actions()
                elif i == 'n':
                    account_actions()
    

def deposit_money():
    print('--------- deposit ---------')
    amt = input('Please type in the amount of money you would like to deposit: ')
    cursor.execute("SELECT * FROM user_info")
    result = cursor.fetchall()
    for row in result:
        sql = "UPDATE user_info SET account_balance = account_balance + %s WHERE id = %s" % (amt, userID)
        cursor.execute(sql)
        connection.commit()
        check_balance()

def withdraw_money():
    print('--------- withdraw ---------')
    amt = input('Please type in the amount of money you would like to withdraw: ')
    select = "SELECT account_balance FROM user_info WHERE id = %s" % (userID)
    cursor.execute(select)
    balance = cursor.fetchone()[0] #integer
    if int(amt) < int(balance):
        sql = "UPDATE user_info SET account_balance = account_balance - %s WHERE id = %s" % (amt, userID)
        ## FOR SOME REASON, IT IS ADDING TO THE ACCOUNT BALANCE, BY THE WRONG AMT

        cursor.execute(sql)
        connection.commit()
    else:
        print('There is not enough money in your account to be withdrawn.')
        account_actions()

### ACCOUNT SETTINGS
def account_settings():
    print('--------- account setttings ---------')
    num1 = int(input('\nEnter a number to: \n\n1. View Account Info \n2. Delete Account\n3. Go back to account overview\n\n'))
    if num1 == 1: 
        print('--------- account info ---------')
        cursor.execute("SELECT * FROM user_info")
        result = cursor.fetchall()
        for row in result:
            if row[0] == userID:
                username = row[1]
                print('\nUSERNAME: ' + username)
                password = row[2]
                print('PASSWORD: ' + password +'\n')
        choice1 = input('Would you like to modify your account information? ')
        for i in choice1:
            if i == 'y':
                change_username_or_pswd()
            if i == 'n':
                account_settings()
    if num1 == 2:
        delete_account()
        printing()
    if num1 == 3:
        account_actions()

## need to fix
def change_username_or_pswd():
    num2 = int(input('\n1. Change Username \n2. Change Password\n'))
    if num2 == 1:
        Nusername = input('\nNew Username: ')
    if num2 == 2:
        Npassword = input('\nNew Password: ')
    cursor.execute("SELECT * FROM user_info")
    result = cursor.fetchall()
    for row in result:
        if row[0] == userID:
            sql = "UPDATE user_info SET user_name = '%s', password = '%s'" % (Nusername, Npassword)
        
        ## fix for num2
        if row[1] == Nusername and row[2] == Npassword and row[0] != userID:
            print("\nPlease select a different username of password.")
            change_username_or_pswd()
    account_settings()

def delete_account():
    sql = "DELETE FROM user_info WHERE id = '%d'" % (userID)
    cursor.execute(sql)
    connection.commit()
    print(cursor.rowcount, "record(s) deleted")

## PRINTING TO CONSOLE
def printing():
    print('--------- BANKING APP ---------')
    num1 = int(input('\nEnter a number to: \n\n1. Log In \n2. Create Account\n\n'))
    checkLogInNumber(num1)


connection = mysql.connector.connect(
    user = 'c2cuser',
    database = 'c2c 1',
    password = 'passw0rd'
)

cursor = connection.cursor()

printing()

cursor.close()
connection.close()
