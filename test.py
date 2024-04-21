from tkinter import *
from WebScraper import Scraper
from PIL import ImageTk, Image

import concurrent.futures

def update_image(query: str) -> None:
    count = 0
    
    scraper = Scraper("chrome")    # Create a new WebScraper instance for each query
    scraper.setSearchQuery(query)
    
    while count != 3:
        data = scraper.getData()

        if data is not None:
            image = Image.open(data)
            scraper.closeDriver()  # Close the WebScraper instance

            print("Image grabbed successfully")
            return image.resize((150,100))
        
        count +=1

    # After four failed attempts create a blank image and return
    image = Image.new("RGB", (150, 100), (0, 0, 0))
    scraper.closeDriver()          # Close the WebScraper instance

    print("Failed to grab image")
    return image

root = Tk()                                                                              # Initialize tkinter

canvas = Canvas(root, width = 1920, height = 1080)                                       # Create a canvas for the tkinter window
canvas.pack(expand = True)

search_queries = ["1995 kawasaki vulcan 800cc black", "2017 subaru wrx black", "2018 Toyota Camry Hybrid Blue", "2012 Ford F250 white", "2013 jeep wrangler black"]
images = [] # Used to keep a reference of each image
y = 10

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_images = [executor.submit(update_image, query) for query in search_queries]

    for image in future_images:
        image = image.result()
        tk_image = ImageTk.PhotoImage(image)
        images.append(tk_image)

        Label(image = tk_image, width = 150, height = 100).place(x = 10, y = y)
        y += 110

root.mainloop()