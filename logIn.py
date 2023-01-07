import sys
from main import DBhelper

class login:

    def __init__(self):
        #connect to the database
        self.db=DBhelper()
        self.menu()

    def menu(self):

        user_input=input("""
        1. Enter 1 to register
        2. Enter 2 to login
        3. Enter 3 to anything else
        """)

        if user_input=="1":
            self.register()
        elif user_input=="2":
            self.search()
        else:
            sys.exit(404)
    def register(self):

        name=input("Enter the name")
        password=input("Enter the password")
        response=self.db.register(name,password)

        if response==1:
            print("registered")
        else:
            print("failed")

        self.menu()

    def search(self):
        name=input("Enter the name")
        password=input("Enter the password")

        self.db.search(name,password)

obj = login()