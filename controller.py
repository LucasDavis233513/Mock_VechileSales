from PIL import ImageTk, Image
from WebScraper import Scraper
import concurrent.futures

import re as regex

class Controller:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
        self.view.setController(self)

        self.images = []            # Used to keep a reference of each image
        self.table = []

        self.updateView()

    def __updateImage(self, query: str) -> Image:
        """
        Helper function to fetch the image results from the web.
        
        If we were unable to fetch a requested image, it will create a blank one to return instead
        """
        count = 0
    
        scraper = Scraper()
        scraper.setSearchQuery(query)       # Set the query to the Scraper
        
        while count != 3:
            data = scraper.getData()        # Attempt to grab the image bytes

            if data is not None:
                image = Image.open(data)
                scraper.closeDriver()

                # Update the progess bar
                return image.resize((150, 100))
            
            count += 1

        # After four failed attempts, create a blank image to use instead
        image = Image.new("RGB", (150, 100), (0, 0, 0))
        scraper.closeDriver()          # Close the WebScraper instance

        # Update the progress bar
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

    def updateView(self):
        """
        Update the mainView with entries from the database

        Initially the view need to fetch the first five entries from the database.
            If the next button is clicked it will need to collect the next five entries
            If the previous button is clicked it will need to collect the previous five entries
        
        If a search is made, it will instead display five entries the results list
            following the same notation for each of the buttons, but instead with this results list.
            If the search field is cleared it needs to return to the default of querying the database.
        """
        # If the table list is empty, run the default method
        #   We need to break the detail, seller, and car id's off of each tuple (should be indecies 0, 5, 6)
        if not self.table:
            rltList = self.model.fetchVechiles(self.view.next, self.view.prev)

            # Reset the next and prev variables 
            self.view.next = False
            self.view.prev = False

        # # If the table list has entries, use it to display the entries instead of querying the database
        # else:
        #     rltList = self.table

        indToExt = [0, 5, 6]
        search = []

        self.Ids, self.Values = self.__ExtractNRemove(rltList, indToExt)

        # Extract the make model and year and concatenate them to a single string
        #   This will be used as our query for the getImage operation
        for item in self.Values:
            query = f"{item[0]}" + f" {item[1]}" + f" {item[2]}"
            search.append(query)

        self.grabImages(search)

        # Call the update method from the view to place the values (list of tuples) and Images (list of images)
        #   onto the MainView subframe
        self.view.updateMainView(self.Values, self.images)

    def search(self, query: str) -> None:
        # If the query is blank, clear the table list
        if query is "":
            self.table.clear()
            self.updateView()
            return

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

        # Append the search results
        self.table.append(self.model.search(**qryDict))
        self.updateView()

    def grabImages(self, search_queries: list) -> None:
        """
        Using the concurrent furtures library, create a list of images by scrapping google images.

        Arguments:
            - search_queries: a list of queries that will be sumbited to the scrapper
        """
        # Ensure that the images list is empty before adding new images
        self.images.clear()

        # Create a pool of worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Sumbit a task to the executor, and store its future result in the list future_images
            #   the worker threads will then perform the requested work
            future_images = [executor.submit(self.__updateImage, query) for query in search_queries]

            for image in future_images:
                image = image.result()                  # Wait until the worker threads have returned with the results from __updateImage
                tk_image = ImageTk.PhotoImage(image)    # Create a Tk image from the results
                self.images.append(tk_image)            # append that Tk image to the images list