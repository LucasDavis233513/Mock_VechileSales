import psycopg2
from abc import ABC, abstractmethod

PROGRAMMER_NAME = "Lucas Davis"

class Command(ABC):
    """
    Command interface declares a method for executing a command
    """
    @abstractmethod
    def execute(self) -> None:
        pass

class Receiver():
    """
    Preforms a requested command
    """
    def __init__(self, _connection: psycopg2, _cursor: psycopg2) -> None:
        self.conn = _connection
        self.curr = _cursor

    def displayTable_action(self, _where: str, _searchQuery: str, _opAct: str) -> list:
        """
        Display a complete table
        """
        try:
            if _opAct == None and _searchQuery == None:
                self.curr.execute(f"""
                    SELECT * FROM {_where}
                """)
            elif _opAct != None and _searchQuery == None:
                self.curr.execute(f"""
                    SELECT * FROM {_where} {_opAct}
                """)
            elif _opAct == None and _searchQuery != None:
                self.curr.execute(f"""
                    SELECT * FROM {_where} WHERE {_searchQuery}
                """)
            else:
                self.curr.execute(f"""
                    SELECT * FROM {_where} WHERE {_searchQuery} {_opAct}
                """)

            table = self.curr.fetchall()

            return table
        except psycopg2.Error as ex:
            print(ex)
            return None

    def find_action(self, _what: str, _where: str, _searchQuery: str, _opAct: str) -> str:
        """
        Find information on a specific value
        """
        try:

            if _searchQuery == None and _opAct == None:
                self.curr.execute(f"""
                    SELECT {_what}
                    FROM {_where}
                """)
            elif _searchQuery == None and _opAct != None:
                self.curr.execute(f"""
                    SELECT {_opAct}({_what})
                    FROM {_where}
                """)
            elif _searchQuery != None and _opAct == None:
                self.curr.execute(f"""
                    SELECT {_what}
                    FROM {_where}
                    WHERE {_searchQuery}
                """)
            else:
                self.curr.execute(f"""
                    SELECT {_opAct}({_what})
                    FROM {_where}
                    where {_searchQuery}
                """)                

            item = self.curr.fetchall()

            return item
        except psycopg2.Error as ex:
            print(ex)
            return "Error"
    
    def insert_action(self, _where: str, _values: tuple) -> str:
        """
        Insert the tuple _values into a given table
        """
        try:
            self.curr.execute(f"""
                INSERT INTO {_where} VALUES {_values}
            """)
            self.conn.commit()

            return None
        except psycopg2.Error as ex:
            print(ex)
            return "Error"
    
    def remove_action(self, _where: str, _searchQuery: str) -> str:
        """
        Remove a tuple 
        """
        try:
            self.curr.execute(f"""
                DELETE FROM {_where}
                WHERE {_searchQuery}
            """)
            self.conn.commit()

            return None
        except psycopg2.Error as ex:
            print(ex)
            return "Error"
        
    def update_action(self, _what: str, _values: list, _search: list, _searchItem: list) -> str:
        """
        Update a list of tuples in a given table
        """
        try:
            count = 0
            for item in _values:
                self.curr.execute(f"""
                    UPDATE {_what}
                    SET {item}
                    WHERE {_search[0]} = '{_searchItem[count][0]}' AND {_search[1]} = {_searchItem[count][1]}
                """)
                self.conn.commit()

                count += 1
            
            return None
        except psycopg2.Error as ex:
            print(ex)
            return "Error"
        
    def exists_Action(self, _where: str, _searchQuery: str) -> bool:
        """
        checks to see if a value exists
        """
        self.curr.execute(f"""
            SELECT *
            FROM {_where}
            WHERE {_searchQuery}
        """)

        # If the value wasn't found
        if self.curr.fetchall() == []:
            return False
        
        # If the value exists
        return True

class Invoke():
    """
    Triggers the execution of a command
    """
    cmd = None

    def setCMD(self, _command: Command) -> None:
        self.cmd = _command

    def exCMD(self):
        return self.cmd.execute()
    
class displayTable(Command):
    """
    Diplay a complete table

    SELECT * FROM _ <WHERE searchQuery> <optionalAction>

    Parameters:
        receiver:
        where: Used to query the correct table
        optionalAction: Defines an optional action that can be preformed on the table

    Returns a list of tuples on success, returns empty list on fail
    """
    def __init__(self, receiver: Receiver, where: str, searchQuery: str = None, optionalAction: str = None) -> None:
        self._receiver = receiver
        self._where = where
        self._searchQuery = searchQuery
        self._opAct = optionalAction
    
    def execute(self) -> list:
        return self._receiver.displayTable_action(self._where, self._searchQuery, self._opAct)

class findValue(Command):
    """
    Find specific information from the database

    SELECT <optionalAction> _ FORM _ <WHERE searchQuery>

    Parameters:
        - receiver
        - what: Used to find the desired entry form the tuple
        - where: Used to query the correct table
        - searchQuery: 
        - optionalAction: Defines an optional action to preform on the data found in the query
                        For example, preforming a SUM or MAX operation on the data

    Returns the request item on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, what: str, where: str, searchQuery:str = None, optionalAction: str = None) -> None:
        self._receiver = receiver
        self._what = what
        self._where = where
        self._searchQuery = searchQuery
        self._opAct = optionalAction

    def execute(self) -> str:
        return self._receiver.find_action(self._what, self._where, self._searchQuery, self._opAct)

class insertData(Command):
    """
    Used to insert data into a table

    INSERT INTO _ VALUES _

    Parameters:
        - receiver
        - where: Used to query the correct table:                 exTable(column1, column2, etc)
        - values: a tuple of values to insert into the table:     ('item1', 'item2', etc)
    
    Returns None on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, where: str, values: tuple) -> None:
        self._receiver = receiver
        self._where = where
        self._values = values

    def execute(self) -> str:
        return self._receiver.insert_action(self._where, self._values)

class removeData(Command):
    """
    Used to remove a specified record

    DELETE FROM _ WHERE _

    Parameters:
        - receiver
        - where: Used to query the correct table
        - searchQuery:

    Returns None on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, where: str, searchQuery: str) -> None:
        self._receiver = receiver
        self._where = where
        self._searchQuery = searchQuery

    def execute(self) -> str:
        return self._receiver.remove_action(self._where, self._searchQuery)
    
class updateData(Command):
    """
    Used to update a table

    UPDATE _ SET _ WHERE _ = _ AND _ = _

    Parameters:
        - receiver
        - what: Used to query the correct table
        - value: columnName = newEntry
        - search: Used to find a specific tuple
        - searchItem: The item you are searching by

    Returns None on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, what: str, value: list, search: list, searchItem: list) -> None:
        self._receiver = receiver
        self._what = what
        self._values = value
        self._search = search
        self._searchItem = searchItem

    def execute(self) -> str:
        return self._receiver.update_action(self._what, self._values, self._search, self._searchItem)
    
class exists(Command):
    """
    Used to check if a value exists within the database

    SELECT * FROM _ WHERE _

    Parameters:
        - receiver
        - where:
        - searchQuery:

    returns True if the value exists, False if it doesn't
    """
    def __init__(self, receiver: Receiver, where: str, searchQuery: str) -> None:
        self._receiver = receiver
        self._where = where
        self._searchQuery = searchQuery

    def execute(self) -> bool:
        return self._receiver.exists_Action(self._where, self._searchQuery)