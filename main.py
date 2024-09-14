import tkinter as tk
from model import CowModel
from controller import CowController
from view import CowView

if __name__ == "__main__":
    root = tk.Tk()
    model = CowModel("cow_data.csv")
    controller = CowController(model)
    view = CowView(root, controller)
    root.mainloop()
