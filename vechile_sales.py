from controller import Controller
from model import Model
from view import View

PROGRAMMER_NAME = "Lucas Davis"

model = Model()
view = View()
controller = Controller(model, view)

view.mainloop()

model.closeConnection()

print(f"Progreammed by: {PROGRAMMER_NAME}")