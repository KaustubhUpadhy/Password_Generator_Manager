import random
import datetime
import mysql.connector
import getpass

def password_generation():
    print("Recommended to have a Password Length above 12 characters")
    passwd_length = int(
        input("How many characters do you want in your password( from 8-16)?: ")
    )
    passwd_restrictions = input("Do you want special characters in your password?: ")
    if passwd_restrictions.upper() == "YES":
        passwd_restrictions = True
        spc, alp, num = length_setter(passwd_length, passwd_restrictions)
        fin_lst = num_chr(num) + alp_chr(alp) + spec_chr(spc)
        random.shuffle(fin_lst)
        password = "".join(fin_lst)
        print("Your Password is : {}".format(password))
    else:
        passwd_restrictions = False
        alp, num = length_setter(passwd_length, passwd_restrictions)
        fin_lst = num_chr(num) + alp_chr(alp)
        random.shuffle(fin_lst)
        password = "".join(fin_lst)
        print("Your Password is : {}\n".format(password))


def num_chr(max_limit):
    all_num = []
    prev = None
    for i in range(0, max_limit):
        value = random.randint(0, 9)
        while value == prev or value in all_num:
            value = random.randint(0, 9)
        all_num.append(str(value))
        prev = value
    return all_num


def alp_chr(max_limit):
    all_alp = []
    prev = None
    for i in range(0, max_limit // 2):
        value = chr(random.randint(65, 90))
        while value == prev or value in all_alp:
            value = chr(random.randint(65, 90))
        all_alp.append(value)
        prev = value
    for i in range(0, max_limit - (max_limit // 2)):
        value = chr(random.randint(97, 122))
        while value == prev or value in all_alp:
            value = chr(random.randint(97, 122))
        all_alp.append(value)
        prev = value
    return all_alp


def spec_chr(max_limit):
    spc_lst = ["@", "^", "#", "$", "!", "%", "*", "&"]
    all_spc = []
    prev = None
    for i in range(0, max_limit):
        value = random.choice(spc_lst)
        while value == prev or value in all_spc:
            value = random.choice(spc_lst)
        all_spc.append(value)
        prev = value
    return all_spc


def length_setter(max_chr, passwd_restrictions):
    total = 0
    if passwd_restrictions == True:
        while total != max_chr:
            spc_max = random.randint(2, max_chr // 2)
            alp_max = random.randint(2, max_chr // 2)
            num_max = random.randint(2, max_chr // 2)
            total = spc_max + alp_max + num_max
        return spc_max, alp_max, num_max
    else:
        while total != max_chr:
            alp_max = random.randint(2, max_chr // 2)
            num_max = random.randint(2, max_chr // 2)
            total = alp_max + num_max + max_chr % 2
        return alp_max + max_chr % 2, num_max


def strength_checker(password):
    points = 0
    if len(password) >= 12:
        points += 1

    # check num characters
    # check special characters
    # check alpha lowercase characters
    # check alpha uppercase characters
    # regex for all above
    # unpredicatbility, no repetiton
    if points <= 2:
        print("Weak Password, Improvement required !!")
    elif points >= 2 & points <= 4:
        print("Good but can be improved !!")
    elif points >= 4 & points <= 6:
        print("Strong Password")
    else:
        print("Excellent Password !!")


time = datetime.datetime.now()
modify_time = time.strftime("%Y-%m-%d %H:%M:%S")


class Password_Management:
    def __init__(self):
        self.username = getpass.getpass("Enter your SQL username: ")
        self.sql_pswd = getpass.getpass("Enter your SQL Password: ")
        try:
            self.con1 = mysql.connector.connect(
                host="localhost", user=self.username, passwd=self.sql_pswd
            )
            if self.con1.is_connected():
                print("Conncetion Established")
            self.my_cursor = self.con1.cursor()
            self.my_cursor.execute("Create Database if not exists Password_Storage;")
            self.my_cursor.execute("use Password_Storage;")
        except mysql.connector.Error as er:
            print(
                "Sorry, there was an {} error that occured while connecting to the MySQL Database!!".format(
                    er.msg
                )
            )
            print("Please try again")
            self.__init__()

    def storage_mgmt(self):
        print(
            "1. Do you want to create a new table?\n2. Do you want to delete an existing table?"
        )
        choice = int(input("What do you want to do? : "))
        if choice == 1:
            tables = int(input("Enter the number of tables you want to create: "))
            try:
                for i in range(0, tables):
                    table_name = input("Enter the table name : ")
                    self.my_cursor.execute(
                        "create table if not exists {}(App_Name varchar(50) NOT NULL, username_email varchar(50) NOT NULL, Password varchar(50) NOT NULL, Last_Modified datetime);".format(
                            table_name
                        )
                    )
                print("Operation performed succesfully!!\n")
            except mysql.connector.Error as er:
                print(
                    "Sorry, there was an {} error that occured while performing this operation!!".format(
                        er.msg
                    )
                )
                print("Please try again")
                self.storage_mgmt()
        elif choice == 2:
            final = input("Are you sure you want to Delete an entire table?:")
            if final.upper() == "YES":
                self.my_cursor.execute("SHOW TABLES;")
                tables = self.my_cursor.fetchall()
                for table in tables:
                    print(table[0])
                try:
                    table_name = input(
                        "Enter the table name you want to Delete or Drop: "
                    )
                    self.my_cursor.execute("DROP TABLE {};".format(table_name))
                    print("Operation performed succesfully!!\n")
                except mysql.connector.Error as er:
                    print(
                        "Sorry, there was an {} error that occured while performing this operation!!".format(
                            er.msg
                        )
                    )
                    print("Please try again")
                    self.storage_mgmt()

    def save_password(self):
        self.my_cursor.execute("SHOW TABLES;")
        tables = self.my_cursor.fetchall()
        print("Showing all tables:\n")
        for table in tables:
            print(table[0])
        table_name = input(
            "Enter the table name you want to add/save the password to: "
        )
        appname = input("Enter the name of Application: ")
        user_email = input("Enter username or email: ")
        password = input("Enter the Password: ")
        query = "INSERT INTO {} VALUES (%s,%s,%s,%s);".format(table_name)
        values = (appname, user_email, password, modify_time)
        try:
            self.my_cursor.execute(query, values)
            self.con1.commit()
            print("Operation Successfull!! Password succesfully added to the database.")
        except mysql.connector.Error as er:
            print(
                "Sorry, there was an {} error that occured while performing the operation".format(
                    er.msg
                )
            )
            print("Please try again")
            self.save_password()

    def password_removal(self):
        table_name = input(
            "Enter the table name you want to Delete the password from: "
        )
        appname = input("Enter the name of Application: ")
        user_email = input("Enter the username or email associated with the password:")
        query = "DELETE FROM {} WHERE App_Name = %s and username_email = %s;".format(
            table_name
        )
        values = (appname, user_email)
        try:
            self.my_cursor.execute(query, values)
            self.con1.commit()
            print(
                "Operation Successfull!! Password succesfully Deleted from the database."
            )
        except mysql.connector.Error as er:
            print(
                "Sorry, there was an {} error that occured while performing the operation".format(
                    er.msg
                )
            )
            print("Please try again")
            self.password_removal()

    def extraction(self):
        table_name = input(
            "Enter the table name you want to extract/get the password from: "
        )
        appname = input("Enter the name of Application: ")
        query = "SELECT Password FROM {} WHERE App_Name = %s; ".format(table_name)
        values = (appname,)
        try:
            self.my_cursor.execute(query, values)
            records = self.my_cursor.fetchall()
            for record in records:
                print("Your Password is: " + record[0])
        except mysql.connector.Error as er:
            print(
                "Sorry, there was an {} error that occured while performing the operation".format(
                    er.msg
                )
            )
            print("Please try again")
            self.extraction()


storage = Password_Management()


def Menu():
    print(
        "1. Do you want to generate a Password? \n2. Do you want to edit the Password Storage Database?"
    )
    print(
        "3. Do you want to check Password's Strength?\n4. Do you want to extract/get a Password from the Password Storage?\n5. Do you want to save a Password?"
    )
    print(
        "6. Do you want to delete a Password from the storage?\n7. Do you want to exit?:"
    )
    generation = int(input("What do you want to do?:"))
    if generation == 1:
        password_generation()
        Menu()
    elif generation == 2:
        storage.storage_mgmt()
        Menu()
    elif generation == 3:
        password = input("Please enter the password: ")
        strength_checker(password)
        Menu()
    elif generation == 4:
        storage.extraction()
        Menu()
    elif generation == 5:
        storage.save_password()
        Menu()
    elif generation == 6:
        storage.password_removal()
        Menu()
    elif generation == 7:
        storage.my_cursor.close()
        storage.con1.close()
        exit()
    else:
        print("Incorrect input/choice, Please try again")
        Menu()


Menu()


# Add comments explanations

# password strength check - regex


# Implement cloud services and take this database possibly on the cloud
