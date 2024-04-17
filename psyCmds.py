import psycopg2
from abc import ABC, abstractmethod

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

    def displayTable_action(self, _where: str) -> list:
        """
        Display a complete table
        """
        try:
            self.curr.execute(f"""
                SELECT * FROM {_where}
            """)
            table = self.curr.fetchall()

            return table
        except psycopg2.Error as ex:
            print(ex)
            return None
        
    def displayTuple_action(self, _where: str, _search: str, _searchItem: str) -> list:
        """
        Display specific tuples
        """
        try:
            self.curr.execute(f"""
                SELECT *
                FROM {_where}
                WHERE {_search} = '{_searchItem}'
            """)
            tuples = self.curr.fetchall()
 
            return tuples
        except psycopg2.Error as ex:
            print(ex)
            return None

    def find_action(self, _what: str, _where: str, _search: str, _searchItem: str, _opAct: str) -> str:
        """
        Find information on a specific value
        """
        try:
            if _opAct == None:
                self.curr.execute(f"""
                    SELECT {_what}
                    FROM {_where}
                    where {_search} = '{_searchItem}'
                """)
            elif _search == None and _searchItem == None:
                self.curr.execute(f"""
                    SELECT {_opAct}({_what})
                    FROM {_where}
                """)
            elif _search == None and _searchItem == None and _opAct == None:
                self.curr.execute(f"""
                    SELECT {_what}
                    FROM {_where}
                """)                
            else:
                self.curr.execute(f"""
                    SELECT {_opAct}({_what})
                    FROM {_where}
                    where {_search} = '{_searchItem}'
                """)

            item = self.curr.fetchone()[0]

            return item
        except psycopg2.Error as ex:
            print(ex)
            return "Error"
    
    def findContains_action(self, _what: str, _where: str, _search: str, _searchItem: str) -> str:
        """
        Find information from a record that contains the searchItem
        """
        try:
            self.curr.execute(f"""
                SELECT {_what}
                FROM {_where}
                WHERE {_search} LIKE '%{_searchItem}%'
            """)
            item = self.curr.fetchone()[0]

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
    
    def remove_action(self, _where: str, _search: str, _searchItem: str) -> str:
        """
        Remove a tuple 
        """
        try:
            self.curr.execute(f"""
                DELETE FROM {_where}
                WHERE {_search} = '{_searchItem}'
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
        
    def nutrientData_action(self, _searchItem: str) -> list:
        try:
            self.curr.execute(f"""
                select sum(protien_value) as protien_total, sum(fat_value) as fat_total, sum(carbohydrate_value) as carbohydrate_total
                from nutrientData
                where nutrientData_id in (
                    select nutrientData_id
                    from Foods_nutrientData
                    where fdc_id in (
                        select fdc_id
                        from Foods_userLogs
                        where log_id in (
                            select log_id
                            from userLogs
                            where logDate = '{_searchItem}'
                        )
                    )
                )
            """)
            tuples = self.curr.fetchall()

            return tuples
        except psycopg2.Error as ex:
            print(ex)
            return None

class Invoke():
    """
    Triggers the execution of a command
    """
    cmd = None

    def setCMD(self, _command: Command) -> None:
        self.cmd = _command

    def exCMD(self) -> str:
        return self.cmd.execute()
    
class displayTable(Command):
    """
    Diplay a complete table

    SELECT * FROM _

    Parameters:
        receiver:
        where: Used to query the correct table

    Returns a list of tuples on success, returns empty list on fail
    """
    def __init__(self, receiver: Receiver, where: str) -> None:
        self._receiver = receiver
        self._where = where
    
    def execute(self) -> list:
        return self._receiver.displayTable_action(self._where)
    
class displayTuple(Command):
    """
    Display a list of tuples from a search query

    SELECT * FROM _ WHERRE _ = '_'

    Parameters:
        - reciever
        - where: Used to query the correct table
        - search: Used to find a specific tuple
        - searchItem: The item you are searching by

    returns a list of tuples from a search on success, returns empty list on fail
    """
    def __init__(self, reciever: Receiver, where: str, search: str, searchItem: str) -> None:
        self._receiver = reciever
        self._where = where
        self._search = search
        self._searchItem = searchItem

    def execute(self) -> list:
        return self._receiver.displayTuple_action(self._where, self._search, self._searchItem)

class findValue(Command):
    """
    Find specific information from the database

    SELECT <optionalAction> _ FORM _ WHERE _ = '_'

    Parameters:
        - receiver
        - what: Used to find the desired entry form the tuple
        - where: Used to query the correct table
        - search: Used to find a specific tuple
        - searchItem: The item you are searching by
        - optionalAction: Defines an optional action to preform on the data found in the query
                        For example, preforming a SUM or MAX operation on the data

    Returns the request item on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, what: str, where: str, search: str, searchItem: str, optionalAction: str) -> None:
        self._receiver = receiver
        self._what = what
        self._where = where
        self._search = search
        self._searchItem = searchItem
        self._opAct = optionalAction

    def execute(self) -> str:
        return self._receiver.find_action(self._what, self._where, self._search, self._searchItem, self._opAct)

class findContains(Command):
    """
    Used to find a value based of a record that contains a specified value

    SELECT _ FROM _ WHERE _ LIKE '%_%'

    Parameters:
        - receiver
        - what: Used to find the desired entry form the tuple
        - where: Used to query the correct table
        - search: Used to find a specific tuple
        - searchItem: The item you are searching by

    Returns the requested item on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, what: str, where: str, search: str, searchItem: str) -> None:
        self._receiver = receiver
        self._what = what
        self._where = where
        self._search = search
        self._searchItem = searchItem

    def execute(self) -> str:
        return self._receiver.findContains_action(self._what, self._where, self._search, self._searchItem)

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

    DELETE FROM _ WHERE _ = '_'

    Parameters:
        - receiver
        - where: Used to query the correct table
        - search: Used to find a specific tuple
        - searchItem: The item you are searching by

    Returns None on success, the string 'Error' on fail
    """
    def __init__(self, receiver: Receiver, where: str, search: str, searchItem: str) -> None:
        self._receiver = receiver
        self._where = where
        self._search = search
        self._searchItem = searchItem

    def execute(self) -> str:
        return self._receiver.remove_action(self._where, self._search, self._searchItem)
    
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
    
class nutrientData(Command):
    """
    Used to find the nutrient information for a given table

    select sum(protien_value) as protien_total, sum(fat_value) as fat_total, sum(carbohydrate_value) as carbohydrate_total
    from nutrientData
    where nutrientData_id in (
        select nutrientData_id
        from Foods_nutrientData
        where fdc_id in (
            select fdc_id
            from Foods_userLogs
            where log_id in (
                select log_id
                from userLogs
                where logDate = '_'
            )
        )
    )

    Parameters:
        - reciever
        - searchItem: The item you are searching by

    returns a list of tuples on success, None on fail
    """
    def __init__(self, receiver: Receiver, searchItem: str) -> None:
        self._receiver = receiver
        self._searchItem = searchItem

    def execute(self) -> list:
        return self._receiver.nutrientData_action(self._searchItem)