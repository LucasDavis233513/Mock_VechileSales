from tkinter import *
from WebScraper import Scraper
from PIL import ImageTk, Image
import customtkinter as ctk

import concurrent.futures

def update_image(query: str) -> None:
    count = 0
    
    scraper = Scraper()    # Create a new WebScraper instance for each query
    scraper.setSearchQuery(query)
    
    while count != 3:
        data = scraper.getData()

        if data is not None:
            image = Image.open(data)
            scraper.closeDriver()  # Close the WebScraper instance

            print("Image grabbed successfully")
            return image.resize((150,100))
        
        count +=1

    # After four failed attempts, create a blank image to use instead
    image = Image.new("RGB", (150, 100), (0, 0, 0))
    scraper.closeDriver()          # Close the WebScraper instance

    print("Failed to grab image")
    return image

root = Tk()                                                                              # Initialize tkinter

search_queries = ["1995 kawasaki vulcan 800cc black", "2017 subaru wrx black", "2018 Toyota Camry Hybrid Blue", "2012 Ford F250 white", "2013 jeep wrangler black"]
images = [] # Used to keep a reference of each image
y = 0

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_images = [executor.submit(update_image, query) for query in search_queries]

    for i,image in enumerate(future_images):
        image = image.result()
        tk_image = ImageTk.PhotoImage(image)
        images.append(tk_image)

        Label(root, image = tk_image, width = 150, height = 100).grid(row = y, column = 0,
              columnspan = 2, rowspan = 2, padx = 3, pady = 3)
        
        Label(root, text = search_queries[i]).grid(row = y, column = 2)
        Label(root, text = "Details").grid(row = y + 1, column = 2)

        Button(root, text = "View Details").grid(row = y, column = 3)
        
        y += 2

root.mainloop()