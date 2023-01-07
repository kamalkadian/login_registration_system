import mysql.connector
import sys
class DBhelper:
    def __init__(self):
        try:

            self.conn=mysql.connector.connect(host="localhost",user="root",password="",database="user")
            self.mycursor=self.conn.cursor()

        except:

            print("Some error occured.")
            sys.exit(0)

        else:

            print("connected to database")

    def register(self,name,password):
        try:

            self.mycursor.execute("""
            INSERT INTO `detail` (`id`, `Name`, `password`) VALUES (NULL, '{}', '{}');""".format(name,password))
            self.conn.commit()
        except:
            return -1
        else:
            return 1

    def search(self,email,password):

        self.mycursor.execute("""
        SELECT * FROM `detail` WHERE `Name` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))

        data=self.mycursor.fetchall()

        if len(data)==0:
            print("No record....please register")
            self.register()
        else:
            print(data)
