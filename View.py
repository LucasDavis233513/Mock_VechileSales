import pyautogui
import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import ImageTk, Image

from WebScraper import Scraper
import concurrent.futures

class View(ctk.CTk):
    next = False
    prev = False

    def __init__(self):
        """
        Initializes the main window
        """
        super().__init__() # Calls the initializer method

        width, height = pyautogui.size()
        resolution = f"{width}x{height}"

        self.title("Vechile Sales")
        self.geometry(resolution)

        self.controller = None


        self.grid_rowconfigure(0, minsize = 5, weight = 1)
        self.grid_rowconfigure(1, minsize = 900, weight = 1)
        self.grid_rowconfigure(2, minsize = 5, weight = 1)

        self.grid_columnconfigure(0, minsize = 1400, weight = 1)

        # Create a subframe for the actionBar: search and user
        self.actionBar = ctk.CTkFrame(self)
        self.actionBar.grid(row = 0, column = 0, padx = 100, pady = 10, sticky = "sew")
        self.createActionUIWidgets()

        # Create a subframe for the mainView: display vechiles / detail / user information / purchase history
        self.mainView = ctk.CTkFrame(self)
        self.mainView.grid(row = 1, column = 0, padx = 100, pady = 10, sticky = "nsew")
        self.createMainViewWidgets()

        # Create a subframe for the navigationBar: next and previous buttonsß
        self.navigationBar = ctk.CTkFrame(self)
        self.navigationBar.grid(row = 2, column = 0, padx = 100, pady = 10, sticky = "sew")
        self.createNavigationWidgets()

        # Draw a blank tkinter window
        self.updateMainView()

    def setController(self, controller) -> None:
        """
        Sets a reference object for the controller
        """
        self.controller = controller

    def onSearchButtonClick(self, event):
        """
        SearchButton event: Will call the searchEntry operation from the controller when the button is clicked
        """
        if(self.controller):
            self.controller.search(self.searchBox.get())

    def createActionUIWidgets(self) -> None:
        """
        Populate the actionBar with widgets to search, and access a users information / purchase history
        """
        # Search box to take in search queries from the user
        self.searchBox = ctk.CTkEntry(self.actionBar, textvariable = tk.StringVar(), width = 200)
        self.searchBox.insert(0, "Search...")
        self.searchBox.place(relx = 0.1, rely = 0.7, anchor = "center")

        # Search button to sumbit queries to the controller
        self.searchButton = ctk.CTkButton(self.actionBar, text = "Search")
        self.searchButton.place(relx = 0.2, rely = 0.7, anchor = "center")
        self.searchButton.bind("<button-1>", self.onSearchButtonClick)

        # Button to access user information and purchase history
        self.userAccount = ctk.CTkButton(self.actionBar, text = "User")
        self.userAccount.place(relx = 0.9, rely = 0.7, anchor = "center")

    def createMainViewWidgets(self) -> None:
        """
        
        """
        self.mainView.grid_columnconfigure(0, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(1, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(2, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(3, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(4, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(5, minsize = 100, weight = 1)
        

        self.controller.grabImages()

    def createNavigationWidgets(self) -> None:
        """
        
        """
        self.previousButton = ctk.CTkButton(self.navigationBar, text = "Prev")
        self.previousButton.place(relx = 0.9, rely = 0.7, anchor = "e")

        self.nextButton = ctk.CTkButton(self.navigationBar, text = "Next")
        self.nextButton.place(relx = 0.99, rely = 0.7, anchor = "e")

    def updateMainView(self, _values: list = None, _images: list = None) -> None:
        """
        Update the tkinter window with the provided items.

        Arguments:
            - _values = A list of tuples that contains general information about a given entry
            - _images = A list of Tkimages for a given entry
        
        If both arguments are left none, this will draw the tkinter window without any entries.
        """
        # Force the tkinter window to draw if no values are given
        if _values is None and _images is None:
            self.update_idletasks()
            return
        
        # For each element in the two lists, create an entry that contains an image, a describtion, and a button
        #   that will provid further detail of the given entry
        for y, (value, image) in enumerate(zip(_values, _images)):
            y *= 2  # Update y to ensure that no elements overlap

            Label(self.mainView, image = image, width = 150, height = 100).grid(row = y, column = 0,
                columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "w")
            
            Label(self.mainView, text = value).grid(row = y, column = 2,
                    columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "nsew")

            Button(self.mainView, text = "Details").grid(row = y, column = 4,
                    columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "e")

view = View()
view.mainloop()