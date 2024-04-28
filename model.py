import psycopg2
import re as regex
import psyCmds as cd
from Grab_Ini import ini

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

            print("Connected to the database 'vechile_sales' successfully")
        except:
            print("Couldn't connecto the database...\n")
            exit()
    
    def closeConnection(self) -> None:
        """
        Close the connection to the database
        """
        print("Closing connection to the Database...")
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

    def search(self, make: str, model: str = "", year: str = "") -> None:
        """
        Search the database given vechile by make, model, or year

        returns a list of tuples
        """
        self.invoker.setCMD(cd.findValue(self.receiver, "car_id", "Cars", f"(make::text like '%{make}%' and model::text like '%{model}%' and year::text like '%{year}%')"))
        car_ids = self.invoker.exCMD()

        table = []

        for item in car_ids:
            self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", f"car_id = {item[0]}"))
            table.append(self.invoker.exCMD()[0])

        print(table)

    def insert(self, table: str, values: tuple) -> None:
        """
        
        """
        self.invoker.setCMD(cd.insertData(self.receiver, table, values))
        self.invoker.exCMD()

    def remove(self, table: str):
        pass

    def update(self):
        pass

test = Model()

test.closeConnection()