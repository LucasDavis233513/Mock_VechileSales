from tkinter import *
from WebScraper import WebScraper
from PIL import ImageTk, Image
import io

scrapper = WebScraper("chrome")
root = Tk()

canvas = Canvas(root, width = 300, height = 300)
canvas.pack()

scrapper.setItemToSearch("honda accord white")
tk_image = ImageTk.PhotoImage(Image.open(scrapper.getWebpage()).resize((250,200)))

canvas.create_image(0, 0, anchor = 'nw', image = tk_image)

scrapper.closeDriver()

mainloop()