import tkinter as tk

class SpacedGrid(tk.Frame):
    """
    A custom tkinter Frame that implements a grid layout with customizable spacing.
    """
    def __init__(self, parent, padx=0, pady=0):
        """
        Initialize the SpacedGrid.

        Parameters:
        parent (tkinter object): The parent tkinter object where the SpacedGrid will be placed.
        padx (int): The horizontal padding between grid elements. Default is 0.
        pady (int): The vertical padding between grid elements. Default is 0.
        """
        # Initialize the Frame
        tk.Frame.__init__(self, parent)

        # Set the parent, padding, and create an empty item list
        self.parent = parent
        self.config(relief='sunken', bd=2)
        self.__item_list = []
        self.padx = padx
        self.pady = pady

    def __refresh_items(self):
        """
        Refresh the grid by destroying all widgets and recreating them.
        """
        # Destroy all widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Recreate widgets
        for i, row in enumerate(self.__item_list):
            for j, item in enumerate(row):
                label = tk.Label(self, item, anchor='w')
                label.grid(row=i, column=j, padx=self.padx, pady=self.pady)

    def Clear(self, refresh = True):
        """
        Clear all elements from the grid.

        Parameters:
        refresh (bool): whether to refresh the grid after clearing. Default is True
        """
        # Clear the item list
        self.__item_list = []

        # Refresh the grid
        if(refresh):
            self.__refresh_items()

    def Refresh(self):
        """
        Method to call the private __refresh_items() operation
        """
        self.__refresh_items()

    def insert(self, index, *elements, refresh = True):
        """
        Insert elements into the grid at the specified index.

        Parameters:
        index (int or str): The index at which to insert the elements. If 'end', insert at the end.
        *elements: The elements to insert.
        refresh (bool): whether to refresh the grid after inserting. Default is True
        """
        # Determine the index
        if(index == 'end' or index >= len(self.__item_list)):
            index = len(self.__item_list)  # Set index to the end of the list

        # Split the item list at the index
        temp_lst = []
        if(index != len(self.__item_list)):
            temp_lst = self.__item_list[index:]
        self.__item_list = self.__item_list[:index]

        # Add the new elements and recombine the list
        for item in elements:
            if(isinstance(item, dict)):
                item = list(item.values())  # Exclude keys from dictionary items
            self.__item_list.append(item)
        self.__item_list += temp_lst

        # Refresh the grid
        if(refresh):
            self.__refresh_items()