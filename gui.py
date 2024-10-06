import tkinter as tk
from PIL import Image, ImageTk
import calendar
from datetime import datetime
import pandas as pd
from itertools import islice

def get_menu_data(dining_hall):
    menus = {"Sadler": None, "Commons": None}
    menus["Sadler"] = pd.read_csv("sad_menu.csv")  # Adjust the path if needed
    menus["Commons"] = pd.read_csv("caf_menu.csv")  # Adjust the path if needed
    return menus.get(dining_hall, [])

class DiningHallApp:
    def __init__(self, master):
        self.master = master
        master.title("W&M Dining Hall Meal Tracker")
        master.geometry("400x700")
        self.bg_color = '#F0F0F0'
        self.text_color = 'black'
        self.cart_window = None
        master.configure(bg=self.bg_color)
        main_frame = tk.Frame(master, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(main_frame, text="Select a dining hall:", font=("Arial", 20), bg=self.bg_color, fg=self.text_color)
        self.label.pack(pady=20)

        sadler_img = Image.open("sadler.jpeg").resize((380, 300))
        commons_img = Image.open("commons.jpeg").resize((380, 300))
        cart_img = Image.open("cart.png").resize((50, 50))
        calendar_img = Image.open("calendar.png").resize((50, 50))

        self.sadler_photo = ImageTk.PhotoImage(sadler_img)
        self.commons_photo = ImageTk.PhotoImage(commons_img)
        self.cart_photo = ImageTk.PhotoImage(cart_img)
        self.calendar_photo = ImageTk.PhotoImage(calendar_img)

        self.sadler_label = tk.Label(main_frame, image=self.sadler_photo, bg=self.bg_color)
        self.sadler_label.pack(pady=10)
        self.commons_label = tk.Label(main_frame, image=self.commons_photo, bg=self.bg_color)
        self.commons_label.pack(pady=10)

        self.cart_button = tk.Button(main_frame, image=self.cart_photo, bg=self.bg_color, bd=0, command=self.open_cart)
        self.cart_button.place(relx=1.0, rely=0, anchor='ne', x=-10, y=10)
        self.calendar_button = tk.Button(main_frame, image=self.calendar_photo, bg=self.bg_color, bd=0, command=self.open_calendar)
        self.calendar_button.place(relx=0, rely=0, anchor='nw', x=10, y=10)

        self.create_highlight("Sadler", self.sadler_label)
        self.create_highlight("Commons", self.commons_label)

        self.sadler_label.bind("<Button-1>", lambda e: self.open_sadler())
        self.commons_label.bind("<Button-1>", lambda e: self.open_commons())

        self.meals = {}
        self.cart = []
        self.daily_meals = {}

    def create_highlight(self, text, parent):
        highlight = tk.Frame(parent, bg='black', width=200, height=50)
        highlight.place(relx=0.5, rely=0.5, anchor='center')
        label = tk.Label(highlight, text=text, font=("Arial", 30, "bold"), fg="white", bg='black')
        label.pack(expand=True)
        highlight.bind("<Button-1>", lambda e: "break")
        label.bind("<Button-1>", lambda e: "break")

    def open_sadler(self):
        self.open_dining_options("Sadler")

    def open_commons(self):
        self.open_dining_options("Commons")

    def open_dining_options(self, dining_hall):
        options_window = tk.Toplevel(self.master)
        options_window.title(f"{dining_hall} Menu")
        options_window.geometry("600x400")
        options_window.configure(bg=self.bg_color)

        label = tk.Label(options_window, text=f"Today's Menu at {dining_hall}", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        label.pack(pady=10)

        menu_frame = tk.Frame(options_window, bg=self.bg_color)
        menu_frame.pack(fill=tk.BOTH, expand=True)

        menu_df = get_menu_data(dining_hall)
        menu_df.rename(columns={"Unnamed: 0":"Item Name"}, inplace=True)

        # Display items with a button to view nutritional details
        for i, (index, row) in enumerate(menu_df.iterrows()):
            item_frame = tk.Frame(menu_frame, bg='white', bd=2, relief='raised')
            item_frame.grid(row=i//3, column=i%3, padx=10, pady=10)

            item_label = tk.Label(item_frame, text=row['Item Name'], font=("Arial", 12), bg='white', fg='black')
            item_label.pack(pady=5)

            # Using a lambda function with item to ensure the correct item is passed
            item_button = tk.Button(item_frame, text="View Details", font=("Arial", 10),
                                    command=lambda r=row: self.show_item_details(r))
            item_button.pack(pady=5)

    def show_item_details(self, item):
        details_window = tk.Toplevel(self.master)
        details_window.title(f"{item['Item Name']} Details")
        details_window.geometry("300x300")
        details_window.configure(bg=self.bg_color)

        name_label = tk.Label(details_window, text=item['Item Name'], font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color)
        name_label.pack(pady=10)

        # Displaying nutritional details extracted from the DataFrame row
        nutrition_text = ""
        for col in item.index:
            if col != "Item Name" and not pd.isna(item[col]):
                nutrition_text += f"{col}: {item[col]}\n"

        nutrition_label = tk.Label(details_window, text=nutrition_text, font=("Arial", 12), bg=self.bg_color, fg=self.text_color)
        nutrition_label.pack(pady=10)

        add_to_cart_button = tk.Button(details_window, text="Add to Cart", font=("Arial", 12),
                                       command=lambda: self.add_to_cart(item, details_window))
        add_to_cart_button.pack(pady=10)

        # Label to show added to cart message
        self.added_to_cart_label = tk.Label(details_window, text="", font=("Arial", 10), bg=self.bg_color, fg='green')
        self.added_to_cart_label.pack(pady=5)

    def add_to_cart(self, item, details_window):
        self.cart.append(item)
        self.added_to_cart_label.config(text=f"{item['Item Name']} added to cart!")
        details_window.destroy()  # Close the item details window
        self.open_cart()  # Open the cart window to show updated contents

    def open_cart(self):
        cart_window = tk.Toplevel(self.master)
        cart_window.title("Shopping Cart")
        cart_window.geometry("400x400")
        cart_window.configure(bg=self.bg_color)

        if self.cart:
            total_nutrition = {}
            for item in self.cart:
                item_text = f"{item['Item Name']}"
                tk.Label(cart_window, text=item_text, font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=5)
                # Accumulate the nutritional values for each item in the cart
                for col in item.index:
                    if col != "Item Name" and not pd.isna(item[col]):
                        if col not in total_nutrition:
                            total_nutrition[col] = 0
                        # Handle the item values based on their type
                        value = item[col]
                        if isinstance(value, str):
                            # Remove non-numeric characters and convert to float if it's a string
                            numeric_string = ''.join(filter(str.isdigit, value))
                            if numeric_string:  # Check if the string is not empty
                                numeric_value = float(numeric_string)
                            else:
                                numeric_value = 0.0  # Default to 0 if no numeric string found
                        else:
                            # If it's already a number, just use it
                            numeric_value = float(value)
                        total_nutrition[col] += numeric_value  # Assuming the nutrition values are numeric

            # Display total nutritional facts
            tk.Label(cart_window, text="Total Nutritional Facts:", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=10)
            n = len(total_nutrition)
            total_nutrition = dict(islice(total_nutrition.items(), n-1))
            for nutrient, value in total_nutrition.items():
                tk.Label(cart_window, text=f"{nutrient}: {value:.2f}", font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=5)

        else:
            tk.Label(cart_window, text="Your cart is empty!", font=("Arial", 14), bg=self.bg_color, fg=self.text_color).pack(pady=20)

    def open_calendar(self):
        calendar_window = tk.Toplevel(self.master)
        calendar_window.title("Calendar")
        calendar_window.geometry("400x600")
        calendar_window.configure(bg=self.bg_color)

        now = datetime.now()
        cal = calendar.monthcalendar(now.year, now.month)

        month_year_label = tk.Label(calendar_window, text=f"{calendar.month_name[now.month]} {now.year}", 
                                    font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        month_year_label.pack(pady=10)

        cal_frame = tk.Frame(calendar_window, bg=self.bg_color)
        cal_frame.pack()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            day_label = tk.Label(cal_frame, text=day, font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color)
            day_label.grid(row=0, column=days.index(day))

        for row_idx, row in enumerate(cal):
            for col_idx, day in enumerate(row):
                if day != 0:
                    day_button = tk.Button(cal_frame, text=str(day), 
                                           command=lambda d=day: self.submit_meal(d), 
                                           bg=self.bg_color, fg=self.text_color)
                    day_button.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

    def submit_meal(self, day):
        self.daily_meals[day] = self.daily_meals.get(day, 0) + 1
        # Update the label to show submitted message instead of popup
        self.label.config(text=f"Meal submitted on {day}!", fg='green')

if __name__ == "__main__":
    root = tk.Tk()
    app = DiningHallApp(root)
    root.mainloop()
