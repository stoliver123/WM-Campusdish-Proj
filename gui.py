import tkinter as tk
from PIL import Image, ImageTk
import calendar
from datetime import datetime
import pandas as pd

def get_menu_data(dining_hall):
    menus = {"Sadler": None, "Commons": None}
    menus["Sadler"] = pd.read_csv("our_df.csv")  # Adjust the path if needed
    menus["Commons"] = pd.read_csv("our_df.csv")  # Adjust the path if needed
    return menus.get(dining_hall, [])

class DiningHallApp:
    def __init__(self, master):
        self.master = master
        master.title("W&M Dining Hall Meal Tracker")
        master.geometry("400x700")
        self.bg_color = '#F0F0F0'
        self.text_color = 'black'
        master.configure(bg=self.bg_color)
        main_frame = tk.Frame(master, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(main_frame, text="Select a dining hall:", font=("Arial", 20), bg=self.bg_color, fg=self.text_color)
        self.label.pack(pady=20)

        sadler_img = Image.open("sadler.jpeg").resize((380, 300))
        commons_img = Image.open("commons.jpeg").resize((380, 300))
        cart_img = Image.open("cart.png").resize((50, 50))
        calendar_img = Image.open("calendar.png").resize((50,50))

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

            item_button = tk.Button(item_frame, text="View Details", font=("Arial", 10),
                                    command=lambda r=row: self.show_item_details(r))
            item_button.pack(pady=5)

    def show_item_details(self, item):
        # Create a new window to show the details of the selected item
        details_window = tk.Toplevel(self.master)
        details_window.title(f"{item['Item Name']} Details")
        details_window.geometry("300x250")
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

        # Label to show added to cart message
        self.added_to_cart_label = tk.Label(details_window, text="", font=("Arial", 12), bg='green')
        self.added_to_cart_label.pack(pady=5)

        add_to_cart_button = tk.Button(details_window, text="Add to Cart", font=("Arial", 12),
                                       command=lambda: self.add_to_cart(item))
        add_to_cart_button.pack(pady=10)

    def add_to_cart(self, item):
        self.cart.append(item)
        # Update label text instead of showing a popup
        self.added_to_cart_label.config(text=f"{item['Item Name']} added to cart!")

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
                        # Remove units from strings before converting to float
                        value_str = item[col].replace(" g", "").replace(" mg", "").replace(" kcal", "")
                        try:
                            value = float(value_str)
                            if col not in total_nutrition:
                                total_nutrition[col] = 0
                            total_nutrition[col] += value
                        except ValueError:
                            pass  # Handle non-numeric values

            # Display total nutritional facts
            tk.Label(cart_window, text="Total Nutritional Facts:", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=10)
            for nutrient, value in total_nutrition.items():
                tk.Label(cart_window, text=f"{nutrient}: {value:.2f}", font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=5)

        else:
            tk.Label(cart_window, text="Your cart is empty", font=("Arial", 14), bg=self.bg_color, fg=self.text_color).pack(pady=20)

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

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day, font=("Arial", 10, "bold"), bg=self.bg_color, fg=self.text_color).grid(row=0, column=i, padx=5, pady=5)

        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day != 0:
                    btn_color = self.bg_color
                    if day == now.day and now.month == datetime.now().month and now.year == datetime.now().year:
                        btn_color = 'light blue'  # Highlight today's date
                    btn = tk.Button(cal_frame, text=str(day), width=4, height=2, 
                                    command=lambda y=now.year, m=now.month, d=day: self.select_date(y, m, d, calendar_window),
                                    bg=btn_color, fg=self.text_color, bd=1, relief='solid')
                    btn.grid(row=week_num, column=day_num, padx=1, pady=1)

        self.selected_date_label = tk.Label(calendar_window, text="", font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color)
        self.selected_date_label.pack(pady=10)

        self.meals_text = tk.Text(calendar_window, height=5, width=40, font=("Arial", 12), bg='white', fg=self.text_color)
        self.meals_text.pack(pady=10)

        self.submit_button = tk.Button(calendar_window, text="Submit", font=("Arial", 12), command=self.submit_meal)
        self.submit_button.pack(pady=10)

    def select_date(self, year, month, day, window):
        self.current_date = f"{year}-{month:02d}-{day:02d}"
        self.selected_date_label.config(text=f"Selected Date: {self.current_date}")
        self.show_meals_for_date(self.current_date)

    def show_meals_for_date(self, date_str):
        self.meals_text.delete('1.0', tk.END)
        if date_str in self.daily_meals:
            self.meals_text.insert(tk.END, self.daily_meals[date_str])

    def submit_meal(self):
        meal = self.meals_text.get('1.0', tk.END).strip()
        if meal:
            self.daily_meals[self.current_date] = meal
            tk.messagebox.showinfo("Success", "Meal saved for the selected date!")
        else:
            tk.messagebox.showwarning("Warning", "Please enter a meal before submitting.")

root = tk.Tk()
app = DiningHallApp(root)
root.mainloop()
