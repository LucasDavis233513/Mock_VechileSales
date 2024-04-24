from tkinter import *
from WebScraper import Scraper

class View(Tk):
    def __init__(self):
        """
        Initializes the main window
        """
        super().__init__() # Calls the initializer method from tkinter
        self.stdView()

    def __updateImage(self, query):
        pass

    def stdView(self):
        pass