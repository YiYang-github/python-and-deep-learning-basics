import os
import requests
import tkinter as tk
from PIL import ImageTk, Image
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("不同国家经济指标比较")
        master.geometry("1200x900")

        #add a frame
        self.frame = tk.Frame(master)
        self.frame.pack()

        # add the World Bank Logo to the frame
        self.logo_img = Image.open("image/World-Bank-logo.jpg")
        logo_width, logo_height = self.logo_img.size
        logo_ratio = logo_width / logo_height
        max_logo_width = 400
        if logo_width > max_logo_width: #control the size and resize it to fit within the frame
            logo_width = max_logo_width
            logo_height = int(logo_width / logo_ratio)
        self.logo_img = self.logo_img.resize((logo_width, logo_height))
        self.logo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = tk.Label(self.frame, image=self.logo)
        self.logo_label.pack(side=tk.LEFT, padx=20, pady=20)

        #Add a frame for input/output widgets
        self.input_output_frame = tk.Frame(self.frame)
        self.input_output_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Add a label and entry box for user to input country names
        self.country_label = tk.Label(self.input_output_frame, text="请输入国家名称(英文), 用逗号隔开:")
        self.country_label.pack(pady=10)
        self.country_entry = tk.Entry(self.input_output_frame)
        self.country_entry.pack(pady=10)

        # Add a label and entry box for user to input start and end years
        self.year_label = tk.Label(self.input_output_frame, text="请输入开始和结束年份，以逗号分割:")
        self.year_label.pack(pady=10)
        self.year_entry = tk.Entry(self.input_output_frame)
        self.year_entry.pack(pady=10)

        # Add a button to generate the plot
        self.gen_button = tk.Button(self.input_output_frame, text="生成图像", command=self.generate_image)
        self.gen_button.pack(pady=10)

        # Add a label for displaying the plot
        self.img_frame = tk.Frame(self.frame)
        self.img_frame.pack(side=tk.BOTTOM, padx=20, pady=20)
        self.img_label = tk.Label(self.img_frame)
        self.img_label.pack(side=tk.TOP, pady=20)

    #input:raw_data; output: image
    def plot(self,dict,countries,start_year,end_year):

        gdp,pop,inc,years = [],[],[],[]
        year = [i for i in range(start_year,end_year+1)]

        for country in countries:
            out1,out2,out3 = reverse(dict[country][0]), reverse(dict[country][1]), reverse(dict[country][2])
            #out is list
            gdp.append(out1)
            pop.append(out2)
            inc.append(out3)
            years.append(year)
        
        fig, axs = plt.subplots(3, 1, figsize=(10, 30))
        for ii in range(len(countries)):
            axs[0].plot(year, gdp[ii], label=countries[ii])
        for ii in range(len(countries)):
            axs[1].plot(year, pop[ii], label=countries[ii])
        for ii in range(len(countries)):
            axs[2].plot(year, inc[ii], label=countries[ii])

        # axs[0].plot(years, gdp)
        # axs[1].plot(years, pop)
        # axs[1].plot(years, inc)

        axs[0].set_title('GDP')
        axs[0].legend(loc='best')
        axs[1].set_title('Population')
        axs[1].legend(loc='best')
        axs[2].set_title('Disposable Income')
        axs[2].legend(loc='best')
        # plt.show()
        if not os.path.exists('image'):
            os.makedirs('image')
        axs[0].figure.savefig(f"image/out.png")

    #input:year,countries; output:raw_data
    def get_data(self,start_date: int, end_date: int, countries: List[str]) -> Dict[str, List[List[Tuple[int, float]]]]:
        base_url = "https://api.worldbank.org/v2/country"
        data_type = {"GDP": "NY.GDP.MKTP.CD", "Population": "SP.POP.TOTL", "GNI per capita": "NY.GNP.PCAP.CD"}
        data1 = {}
        
        for country in countries:
            country_data = []
            for key in data_type:
                url = f"{base_url}/{country}/indicator/{data_type[key]}?format=json&per_page=1000&date={start_date}:{end_date}"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    if data[0]["total"] == 0:
                        raise ValueError(f"No {key} data available for {country}")
                    data = data[1]
                    country_data.append([(int(datum['date']), float(datum['value'])) for datum in data])
                except requests.exceptions.RequestException as e: #robustness
                    print(f"Error occurred while retrieving {key} data for {country}: {e}")
                    country_data.append([])
                except (ValueError, KeyError) as e:
                    print(f"Error occurred while processing {key} data for {country}: {e}")
                    country_data.append([])
            data1[country] = country_data
        return data1
    
    #input:country,year; output:saved img
    def generate_image(self):
        
        country = self.country_entry.get()
        year = self.year_entry.get()

        country_list = country.split(",")
        a, b = year.split(",")
        start_date, end_date = int(a.strip()), int(b.strip())

        data = self.get_data(start_date,end_date,country_list)
        self.plot(data,country_list,start_date,end_date)

        #check the generation
        if os.path.isfile("image/out.png"):
            img = Image.open("image/out.png")
            img = img.resize((400, 400))
            img = ImageTk.PhotoImage(img)
            self.img_label.configure(image=img)
            self.img_label.image = img
        else: #robustness
            self.img_label.configure(text="输入有误，无法生成图像！")

#The function takes a list class from a complex data type and reverses the order
def reverse(raw):
    pro = []
    for i in range(len(raw)):
        pro.append(raw[i][1])
    pro = pro[: :-1] 
    return pro

