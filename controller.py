from PIL import ImageTk, Image
from WebScraper import Scraper
import concurrent.futures

import re as regex

import random
from datetime import datetime

PROGRAMMER_NAME = "Lucas Davis"

class Controller:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        self.view.setController(self)

        self.images = []            # Used to keep a reference of each image
        self.usrID = None

        self.updateView()

    def __updateImage(self, query: str) -> Image:
        """
        Helper function to fetch the image results from the web.
        
        If we were unable to fetch a requested image, it will create a blank one to return instead
        """
        count = 0
    
        scraper = Scraper()
        scraper.setSearchQuery(query)       # Set the query to the Scraper
        
        while count != 2:
            data = scraper.getData()        # Attempt to grab the image bytes

            if data is not None:
                image = Image.open(data)
                scraper.closeDriver()

                return image.resize((150, 100))
            
            count += 1

        # After four failed attempts, create a blank image to use instead
        image = Image.new("RGB", (150, 100), (0, 0, 0))
        scraper.closeDriver()          # Close the WebScraper instance

        return image
    
    def __ExtractNRemove(self, _lst: list, _indToExt: list) -> list:
        """
        Extract and remove the elements from a given list of tuples

        Arguments:
            - lst: a list of tuples
            - indToRm: a list of indices that we wish to extract

        returns two list of tuples; extracted elements, a list of tuples with the given indices removed
        """
        extLst = []
        newLst = []

        for tup in _lst:
            extracted = tuple(tup[i] for i in _indToExt)
            new = tuple(tup[i] for i in range(len(tup)) if i not in _indToExt)

            extLst.append(extracted)
            newLst.append(new)

        return extLst, newLst
    
    def findInfo(self, id: str, name: str) -> list:
        """
        Used to find the information about a particular id
        """
        if name == "Seller":
            return self.model.fetchSeller(id)
        elif name == "Detail":
            return self.model.fetchDetails(id)
        
    def updateView(self) -> None:
        """
        Update the mainView with entries from the database

        Initially the view need to fetch the first five entries from the database.
            If the next button is clicked it will need to collect the next five entries
            If the previous button is clicked it will need to collect the previous five entries
        
        If a search is made, it will instead display five entries the results list
            following the same notation for each of the buttons, but instead with this results list.
            If the search field is cleared it needs to return to the default of querying the database.
        """
        # If the car_ids var is an empty list, call the fetchVechiles method of the model
        if self.model.car_ids == []:
            rltList = self.model.fetchVechiles(self.view.next, self.view.prev)

        # else, call the searchNav method
        else:
            rltList = self.model.searchNav(self.view.next, self.view.prev)

        # Reset the next and prev variables 
        self.view.next = False
        self.view.prev = False

        indToExt = [0, 5, 6]
        search = []

        self.Ids, self.Values = self.__ExtractNRemove(rltList, indToExt)

        # Extract the make model and year and concatenate them to a single string
        #   This will be used as our query for the getImage operation
        for item in self.Values:
            query = f"{item[0]} {item[1]} {item[2]}"
            search.append(query)

        self.grabImages(search)

        # Call the update method from the view to place the values (list of tuples) and Images (list of images)
        #   onto the MainView subframe
        self.view.updateMainView(self.Values, self.images, self.Ids)

    def search(self, query: str) -> None:
        """
        Break a given query into one or more values for make, model, and/or year.
        """
        qryDict = {}
        
        if query.count(' ') == 2:
            tempChar = regex.findall(r'[A-Za-z]*', query)
            qryDict["make"], qryDict["model"] = ' '.join(tempChar).split()

            tempInt = regex.findall(r'[0-9]*', query)
            qryDict["year"] = ''.join(str(e) for e in tempInt)

        elif query.count(' ') == 1:
            tempChar = regex.findall(r'[A-Za-z]*', query)
            qryDict["make"], qryDict["model"] = ' '.join(tempChar).split()

        elif query.count(' ') == 0:
            tempChar = regex.findall(r'[A-Za-z]*', query)
            qryDict["make"] = ''.join(tempChar)

        self.model.search(**qryDict)
        self.updateView()

    def grabImages(self, search_queries: list) -> None:
        """
        Using the concurrent furtures library, create a list of images by scrapping google images.

        Arguments:
            - search_queries: a list of queries that will be sumbited to the scrapper
        """
        # Ensure that the images list is empty before adding new images
        self.images.clear()
        self.view.createProgressBar()

        # Create a pool of worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Sumbit a task to the executor, and store its future result in the list future_images
            #   the worker threads will then perform the requested work
            future_images = [executor.submit(self.__updateImage, query) for query in search_queries]

            for x, image in enumerate(future_images):
                progressValue = ((x + 1) / len(future_images)) * 100
                self.view.progressBar["value"] = progressValue
                self.view.update()

                image = image.result()                  # Wait until the worker threads have returned with the results from __updateImage
                tk_image = ImageTk.PhotoImage(image)    # Create a Tk image from the results
                self.images.append(tk_image)            # append that Tk image to the images list

        # Ensure the progress bar reaches 100
        self.view.progressBar["value"] = 100
        self.view.update()

        self.view.progressWindow.destroy()

    def fetchUsrInfo(self) -> None:
        """
        
        """
        # Fetch the users information form the Users table
        usrInfo = self.model.fetchUser(self.usrID)[0]
        keys = ('user_id', 'username', 'password', 'email', 'city', 'state', 'zip_code', 'active')

        # Convert the tuple into a dictionary
        resultDictionary = {keys[i] : usrInfo[i] for i, _ in enumerate(keys)}

        resultDictionary.pop('user_id')
        resultDictionary.pop('active')

        self.view.userInfo = resultDictionary

    def createUser(self, _info: dict) -> None:
        """
        def insert(self, table: str, values: tuple) -> None:
        """
        if _info is None:
            self.view.messageDialog("Failed to create user")
            return
        
        while True:
            usrID = random.randint(10000, 1000000)  # Generate a userID

            if not self.model.checkVal("Users", str(usrID), "user_id"): # Check if that ID is already in use
                break

        # Create a tuple containing all the account information and the userID
        Account = tuple([str(usrID)] + list(_info.values()) + [True])

        self.model.insert("Users", Account)

        self.view.messageDialog("User created successfully")

    def login(self, usrInfo: dict) -> None:
        """
        log in a specific user given a dictionary of their username and password

        Parameter:
            - usrInfo: A dictionary of the users username and password

        returns if the provided username or password wasn't collected or if they don't
        exist in the database
        """
        # Check if we successfully collected the information from the user
        if usrInfo is None:
            self.view.messageDialog("Failed to grab username or password.")
            return

        # Check if the username and password exist in the database
        for field in ['username', 'password']:
            if not self.model.checkVal("Users", usrInfo[field], field):
                self.view.messageDialog("Username or password is incorrect")
                return

        self.usrID = self.model.findUsrID(usrInfo['username'])
        self.view.signedIN = True
        self.view.messageDialog("Logged in successfully")

    def removeUsr(self) -> None:
        """
        Attempt to remove a users account. If a user had made any purchases, their account will
        simply be deactivated.
        """
        if self.usrID is None:
            self.view.messageDialog("There was a problem deleting the current user")
            return
        elif self.model.remove(self.usrID) == "Error":
            self.view.messageDialog("Failed to remove the user")
            return
        
        self.view.messageDialog("The current user was successfully removed")

    def updateInfo(self, newInfo: dict) -> None:
        """
        Update a users account based on the new information from the newInfo dictionary
        """
        for key, val in newInfo.items():
            check = self.model.update(self.usrID, key, val)

            if check == "Error":
                self.view.messageDialog("Failed to update Account information")
                break
        
        self.view.messageDialog("Updated Account information successfully")

    def makePurchase(self, carID: str) -> None:
        """
        Attempt to purchase a vechile

        if the carID doesn't already exist in the Purchases table it will generate a new purchase ID
        and append the current users ID, the car we are purchasesing and the current date
        """
        # Check if a vechile was already purchased
        if self.model.checkVal("Purchases", carID, "car_id"):
            self.view.messageDialog("This vechile is already pruchased")
            return
        
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        while True:
            purchaseID = random.randint(1000000, 10000000)  # Generate a purchaseID

            if not self.model.checkVal("Purchases", str(purchaseID), "purchase_id"): # Check if that ID is already in use
                break

        values = (purchaseID, self.usrID, carID, formatted_datetime)

        self.model.insert("Purchases", values)