import psycopg2
import psyCmds as cd
from Grab_Ini import ini

class model:
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
        print("\nClosing connection to the Database...")
        self.conn.close()

    def fetchLog(self) -> None:
        """
        fetch five entries at a time based off the last five entries gathered and on whether next or previous was pressed.

        If no entries have been gathered initially, it will grab the first five entries.
        If we do have entries previously gathered, if next is pressed, find the highest car_id + 1 and use this as an index to
        grab the next five entries.
        if previous is pressed, find the lowest car_id - 1 and use it as an index to grab the previous five entries.
        
        select *
        from Cars
        where car_id in (
            select car_id
            from Cars
            where car_id > 1004
        ) LIMIT 5;
        """

        self.invoker.setCMD(cd.displayTable(self.receiver, "Cars", "LIMIT 5"))
        table = self.invoker.exCMD()