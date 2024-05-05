import pyautogui
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import ImageTk, Image

from WebScraper import Scraper
import concurrent.futures

PROGRAMMER_NAME = "Lucas Davis"

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

        self.controller = None                  # A reference to the controller
        self.userInfo = None                    # A reference to user collected information
        self.signedIN = None                    # A reference used to see if a user is currently logged in

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

    def onSearchButtonClick(self, event) -> None:
        """
        SearchButton event: Will call the searchEntry method from the controller
        """
        if(self.controller):
            self.controller.search(self.searchBox.get())

    def onPrevButtonClick(self, event) -> None:
        """
        prevButton event: Sets the global var prev to true and call the updateView() method from the controller
        """
        if(self.controller):
            self.prev = True
            self.controller.updateView()

    def onNextButtonClick(self, event) -> None:
        """
        nextButton event: Will set the global var next to true and call the updateView() method from the controller
        """
        if(self.controller):
            self.next = True
            self.controller.updateView()

    def onDetailButtonClick(self, carInfo: tuple):
        """
        detailButton event: Will pass in the information about a particular vechile
        """
        # Break the ids out of the tuple
        carID = carInfo[0]
        sellerID = carInfo[1]
        detailID = carInfo[2]

        # Fetch the infomation about a particular vechile based on its id
        seller = self.controller.findInfo(sellerID, "Seller")
        details = self.controller.findInfo(detailID, "Detail")
        
        # Display the dialog box with the requested informaiton
        self.detailDialog(carID, details, seller)

    def create_dropdown(self, event):
        """
        userAccounts Button event: Will create a drop down menu that will allow a user to login
        logout or create a new user
        """
        menu = tk.Menu(self, tearoff = 0)

        # If no one is signed in, display options to create or login to a user
        if self.signedIN is None:
            menu.add_command(label = "Create User", command = lambda: (self.crtEntryDialog(['username', 'password', 'email', 'city', 'state', 'zip_code'], "Create User"), self.controller.createUser(self.userInfo)))
            menu.add_command(label = "Login", command = lambda: (self.crtEntryDialog(['username', 'password'], "Login"), self.controller.login(self.userInfo)))
        
        # else if someone is signed in, display options to remove that users account or logout or to update that users information
        else:
            menu.add_command(label = "Update User Information", command = lambda: (self.controller.fetchUsrInfo(), self.crtEntryDialog(['username', 'password', 'email', 'city', 'state', 'zip_code'], "Update Info", True), self.controller.updateInfo(self.userInfo)))
            menu.add_command(label = "Delete Account", command = lambda: (self.controller.removeUsr(), setattr(self, 'signedIN', None)))
            menu.add_command(label = "Logout", command = lambda: (setattr(self, 'signedIN', None)))

        menu.post(event.x_root, event.y_root)

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
        self.searchButton.bind("<Button-1>", self.onSearchButtonClick)

        # Button to access user information and purchase history
        self.userAccount = ctk.CTkButton(self.actionBar, text = "User")
        self.userAccount.place(relx = 0.9, rely = 0.7, anchor = "center")
        self.userAccount.bind("<Button-1>", self.create_dropdown)

    def createMainViewWidgets(self) -> None:
        """
        
        """
        self.mainView.grid_columnconfigure(0, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(1, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(2, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(3, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(4, minsize = 100, weight = 1)
        self.mainView.grid_columnconfigure(5, minsize = 100, weight = 1)

    def createNavigationWidgets(self) -> None:
        """
        Populate the navigationBar with the next and previous button
        """
        self.prevButton = ctk.CTkButton(self.navigationBar, text = "Prev")
        self.prevButton.place(relx = 0.88, rely = 0.7, anchor = "e")
        self.prevButton.bind("<Button-1>", self.onPrevButtonClick)

        self.nextButton = ctk.CTkButton(self.navigationBar, text = "Next")
        self.nextButton.place(relx = 0.99, rely = 0.7, anchor = "e")
        self.nextButton.bind("<Button-1>", self.onNextButtonClick)

    def updateMainView(self, _description: list = None, _images: list = None, _ids: list = None) -> None:
        """
        Update the tkinter window with the provided items.

        Arguments:
            - _values = A list of tuples that contains general information about a given entry
            - _images = A list of Tkimages for a given entry
        
        If both arguments are left none, this will draw the tkinter window without any entries.
        """
        # Force the tkinter window to draw if no values are given
        if _description is None and _images is None and _ids is None:
            self.update_idletasks()
            return
        
        # For each element in the two lists, create an entry that contains an image, a describtion, and a button
        #   that will provid further detail of the given entry (this button will also provide a way to "purchase" a vechile)
        for y, (value, image) in enumerate(zip(_description, _images)):
            y *= 2  # Update y to ensure that no elements overlap

            # Places the image
            tk.Label(self.mainView, image = image, width = 150, height = 100).grid(row = y, column = 0,
                columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "w")
            
            # Places the vechiles description, including the price of the vechile
            tk.Label(self.mainView, text = value).grid(row = y, column = 2,
                    columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "nsew")
            
            # Create the details buttons making a unqiue function for each passing the information about that particular vechile
            tk.Button(self.mainView, text = "Details", command = lambda y = _ids[int(y/2)] : self.onDetailButtonClick(y)).grid(row = y, column = 4,
                    columnspan = 2, rowspan = 2, padx = 50, pady = 10, sticky = "e")
    
    def __center(self, toplevel):
        """
        Used to center a toplevel dialog box
        """
        toplevel.update_idletasks()

        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2

        toplevel.geometry("+%d+%d" % (x, y))

    def createProgressBar(self) -> None:
        """
        Progress bar dialog box
        """
        # Create a new popup window for the progress bar
        self.progressWindow = tk.Toplevel(self)
        self.progressWindow.title("Progress bar")

        # Create the prgoress bar within the new window
        self.progressBar = ttk.Progressbar(self.progressWindow, orient = "horizontal", length = 200, mode = "determinate")
        
        self.progressBar.pack(padx = 20, pady = 20)
        self.progressBar["maximum"] = 100
        self.progressBar["value"] = 0

        self.__center(self.progressWindow)

    def detailDialog(self, _car_id: str,  _details: list, _seller: list) -> None:
        """
        Dialog box to display the vechile information about a certain car
        """
        dialog = tk.Toplevel(self)
        dialog.title("Vechile Details")
        dialog.configure(bg = "black")

        # Display the details and seller tuples here
        detailColName = ("transmition", "color", "interior color", "body", "trim", "condition", "odometer", "vin", "mmr")
        sellerColName = ("seller name", "state")

        tk.Label(dialog, text = detailColName).grid(row = 1, column = 1, columnspan = 2, padx = 50, pady = 10)             # Detail column names
        tk.Label(dialog, text = _details[0]).grid(row = 2, column = 1, rowspan = 2, columnspan = 2, padx = 50, pady = 10)  # Values
        tk.Label(dialog, text = sellerColName).grid(row = 4, column = 1, columnspan = 2, padx = 50, pady = 10)             # Seller column names
        tk.Label(dialog, text = _seller[0]).grid(row = 5, column = 1, rowspan = 2, columnspan = 2, padx = 50, pady = 10)   # Seller values

        # Call the purchase functionality
        def on_purchase(_id):
            if not self.signedIN:
                self.messageDialog("You must be signed in to make a purchase")
                return
            
            self.controller.makePurchase(_id)
        
        # Back and previous buttons
        ctk.CTkButton(dialog, text = "Back", command = lambda: dialog.destroy()).grid(row = 7, column = 1, padx = 50, pady = 10)
        ctk.CTkButton(dialog, text = "Purchase", command = lambda: on_purchase(_car_id)).grid(row = 7, column = 2, padx = 50, pady = 10)

        self.__center(dialog)

        dialog.wait_window()

    def crtEntryDialog(self, keys: list, title: str, displayPrv: bool = False) -> None:
        """
        Dialog box to gather a set of infromation from the user
        
        Parameters:
            keys: A list of keys signifying what you wish to collect from the user
            title: the title of the dialog box
        
        Any collected information from the user will be stored in the userInfo variable
        """
        # Create a custom dialog box
        dialog = tk.Toplevel(self)
        dialog.title(title)

        # Set a dark background for the dialog
        dialog.configure(bg = "black")

        # Create text entry fields for each key in the dictionary
        entries = {}
        for i, key in enumerate(keys):
            label = ctk.CTkLabel(dialog, text=f"{key}:")
            label.grid(row=i, column = 0, padx = 10, pady = 5)

            if key == 'Password' or key == 'password':
                entry = ctk.CTkEntry(dialog, show = "*")
            else:
                entry = ctk.CTkEntry(dialog)

            # If displayPrv is True and the key exists in self.userInfo, set the entry value
            if displayPrv and key in self.userInfo:
                entry.insert(0, self.userInfo[key])
            
            entry.grid(row = i, column = 1, padx = 10, pady = 5)
            entries[key] = entry

        # OK button to confirm the entry
        okButton = ctk.CTkButton(dialog, text = "OK", command = lambda: self.onDialogOK(entries, dialog))
        okButton.grid(row=len(keys), column = 0, columnspan = 2, pady = 10)

        # Create a variable to store the entered data
        entryData = {}

        # Function to handle the OK button click
        def on_ok():
            nonlocal entryData
            entryData = {key: entry.get() for key, entry in entries.items()}
            dialog.destroy()

            if all(value != '' for value in entryData.values()):
                # If all keys have values, store the entered data in the instance variable
                self.userInfo = entryData
            else:
                # If one or more keys were left blank, set entryData back to None
                self.userInfo = None

        okButton.configure(command = on_ok)

        self.__center(dialog)

        # Wait for the dialog to be closed
        dialog.wait_window()

    def messageDialog(self, message):
        """
        Dialog box for popup messgaes

        Paramaters:
        message: A str to be displayed on the dialog box
        """
        dialog = tk.Toplevel(self)

        dialog.attributes('-topmost', True)
        dialog.title("Message Box")
        dialog.configure(bg = "black")

        label = ctk.CTkLabel(dialog, text = message)
        label.grid(row = 0, column = 0, padx = 10, pady = 5)

        def on_ok():
            dialog.destroy()

        okButton = ctk.CTkButton(dialog, text = "OK", command = on_ok)
        okButton.grid(row = 1, column = 0, columnspan = 2, pady = 10)

        self.__center(dialog)

        dialog.wait_window()