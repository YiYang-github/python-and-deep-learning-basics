import os
import requests
# import argparse
import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from utils import GUI

#1. Before you run the program, check the Readme.md to make sure you entered the API correctly.
#2. You can easily visualize economic comparisons between countries through the GUI -
#simply by using the command parameters(Args),or by selecting the appropriate economic indicators directly in utils.py on line 99

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()












# import os
# import requests
# from utils import get_data
# import matplotlib.pyplot as plt
# from typing import Dict, List, Tuple


# countries = ["USA", "CHN", "JPN"]
# start_date,end_date = 2000,2005

# data = get_data(start_date, end_date, countries)
# # data = dict(reversed(data.items())) #reversed order
# print(data)

# for category in ["GDP", "Population", "Disposable Income"]:
#             fig, ax = plt.subplots()
#             for country, values in data.items():
#                 ax.plot(values[category], label=country)
#             ax.legend()
#             ax.set_xlabel('Year')
#             ax.set_ylabel(category)
#             fig.savefig(os.path.join("image", f"{category}.png"))
#             plt.close(fig)

# print(data)