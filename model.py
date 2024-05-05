import psycopg2
import re as regex
import psyCmds as cd
from Grab_Ini import ini
from itertools import islice

PROGRAMMER_NAME = "Lucas Davis"

class Model:
    def __init__(self) -> None:
        """
        Class initialization. Attempt to establish a connection to the database
        """
        try:
            dbInfo = ini().grabInfo("config.ini", "Database_Information")

            # connect to the database
            self.conn = psycopg2.connect(**dbInfo)
            self.curr = self.conn.cursor()

            # Initialize the invoker and receiver used to initiate cmds
            self.invoker = cd.Invoke()
            self.receiver = cd.Receiver(self.conn, self.curr)

            self.car_ids = []
            self.itrLimit = 5
        except:
            print("Couldn't connect to the database...\n")
            exit()
    
    def closeConnection(self) -> None:
        """
        Close the connection to the database
        """
        self.conn.close()

    def fetchVechiles(self, next = False, previous = False) -> list:
        """
        fetch five entries at a time based off the last five entries gathered and on whether next or previous was pressed.

        If no entries have been gathered initially, it will grab the first five entries.
        If we do have entries previously gathered, if next is pressed, find the highest car_id + 1 and use this as an index to
        grab the next five entries.
        if previous is pressed, find the lowest car_id - 1 and use it as an index to grab the previous five entries.

        Returns a list of tuples
        """
        # If Next is pressed and there is data in self.table 
        if next == True and previous == False:
            tempList = []
        
            for item in self.table:
                tempList.append(item[0])

            maxNmbr = str(max(tempList))

            self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", f"car_id > {maxNmbr}", "limit 5"))
        # If previous is pressed and there is data in self.table
        elif next == False and previous == True:
            tempList = []
        
            for item in self.table:
                tempList.append(item[0])

            minNmbr = str(min(tempList) - 6)

            self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", f"car_id > {minNmbr}", "limit 5"))
        # If next and previous is not pressed and self.table is None
        else:
            self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", optionalAction = "limit 5"))
            
        self.table = self.invoker.exCMD()
        return self.table

    def fetchDetails(self, detailID: str) -> list:
        """
        
        """
        self.invoker.setCMD(cd.displayTable(self.receiver, "Details", f"detail_id = {detailID}"))
        table = self.invoker.exCMD()

        return table

    def fetchSeller(self, sellerID: str) -> list:
        """
        
        """
        self.invoker.setCMD(cd.displayTable(self.receiver, "Seller", f"seller_id = {sellerID}"))
        table = self.invoker.exCMD()

        return table
    
    def fetchUser(self, usrID: str) -> list:
        """
        
        """
        self.invoker.setCMD(cd.displayTable(self.receiver, "Users", f"user_id = '{usrID}'"))
        table = self.invoker.exCMD()

        return table
    
    def findUsrID(self, usrname: str) -> str:
        self.invoker.setCMD(cd.findValue(self.receiver, "user_id", "Users", f"username = '{usrname}'"))
        usrID = self.invoker.exCMD()[0][0]

        return usrID

    def search(self, make: str, model: str = "", year: str = "") -> None:
        """
        Search the database given vechile by make, model, or year

        returns a list of tuples
        """
        if make == "":
            self.car_ids.clear()
            return

        # Grab the list of car_ids that matches the given search items
        self.invoker.setCMD(cd.findValue(self.receiver, "car_id", "Cars", f"(make::text like '%{make}%' and model::text like '%{model}%' and year::text like '%{year}%')"))
        self.car_ids = self.invoker.exCMD()
    
    def searchNav(self, next: bool = False, previous: bool = False) -> list:
        """
        This function will be called after the search. It job is to iterate through the self.car_ids var that repersents the results of the search.
        By default, if the next and previous buttons weren't pressed. it will display the first five elements.
        If next is pressed it will iterate over the next five. If previous is pressed it will iterate over the previous five.
        """
        self.table.clear()

        if next == True and previous == False:
            self.itrLimit += 5
            
        elif next == False and previous == True:
            self.itrLimit = max(5, self.itrLimit - 5)

        for item in islice(self.car_ids, int(max(0, self.itrLimit - 5)), int(min(self.itrLimit, len(self.car_ids) - 1))):
            self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", f"car_id = {item[0]}"))
            self.table.append(self.invoker.exCMD()[0])
        
        return self.table
    
    def checkVal(self, table: str, val: str, attr: str) -> bool:
        """
        Check if a userID exits in the Users table
        """
        self.invoker.setCMD(cd.exists(self.receiver, table, f"{attr} = '{val}'"))
        return self.invoker.exCMD()
    
    def insert(self, table: str, values: tuple) -> None:
        """
        Insert values into a given table
        """
        self.invoker.setCMD(cd.insertData(self.receiver, table, values))
        self.invoker.exCMD()

    def remove(self, ID: str):
        """
        Remove a user based on the userID
        update Users set active = False where user_id = <ID>;
        """
        # If the user exists in the Purchases table, we need to deactivate their account
        # to keep a record of their purchase.
        if self.checkVal("Purchases", ID, "user_id"):
            self.invoker.setCMD(cd.updateData(self.receiver, "Users", "Active = False", f"user_id = '{ID}'"))

        # Otherwise, if they haven't made any purchases, we can simply remove them.
        else:
            self.invoker.setCMD(cd.removeData(self.receiver, "Users", f"user_id = '{ID}'"))
        
        return self.invoker.exCMD()

    def update(self, ID: str, attr: str, val: str) -> None:
        """
        Update a users information
        """
        self.invoker.setCMD(cd.updateData(self.receiver, "Users", f"{attr} = '{val}'", f"user_id = '{ID}'"))
        self.invoker.exCMD()