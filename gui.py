import tkinter as tk
from PIL import Image, ImageTk
import calendar
from datetime import datetime

def get_menu_data(dining_hall):
    menus = {
        "Sadler": [
            {"name": "Grilled Chicken", "nutrition": "Calories: 165, Protein: 31g, Fat: 3.6g"},
            {"name": "Vegetarian Pasta", "nutrition": "Calories: 320, Protein: 12g, Fat: 6g"},
            {"name": "Caesar Salad", "nutrition": "Calories: 230, Protein: 8g, Fat: 18g"},
            {"name": "Tomato Soup", "nutrition": "Calories: 74, Protein: 2g, Fat: 2g"},
            {"name": "Steamed Broccoli", "nutrition": "Calories: 31, Protein: 2.5g, Fat: 0.3g"},
            {"name": "Chocolate Cake", "nutrition": "Calories: 352, Protein: 4g, Fat: 15g"}
        ],
        "Commons": [
            {"name": "Pepperoni Pizza", "nutrition": "Calories: 285, Protein: 12g, Fat: 10g"},
            {"name": "Veggie Burger", "nutrition": "Calories: 242, Protein: 11g, Fat: 8g"},
            {"name": "Greek Salad", "nutrition": "Calories: 180, Protein: 5g, Fat: 16g"},
            {"name": "Clam Chowder", "nutrition": "Calories: 201, Protein: 10g, Fat: 12g"},
            {"name": "Grilled Salmon", "nutrition": "Calories: 206, Protein: 22g, Fat: 12g"},
            {"name": "Fresh Fruit Cup", "nutrition": "Calories: 60, Protein: 1g, Fat: 0g"}
        ]
    }
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
        options_window.geometry("360x400")
        options_window.configure(bg=self.bg_color)
        label = tk.Label(options_window, text=f"Today's Menu at {dining_hall}", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        label.pack(pady=10)
        menu_frame = tk.Frame(options_window, bg=self.bg_color)
        menu_frame.pack(fill=tk.BOTH, expand=True)
        menu_items = get_menu_data(dining_hall)
        for i, item in enumerate(menu_items):
            item_frame = tk.Frame(menu_frame, bg='white', bd=2, relief='raised')
            item_frame.grid(row=i//3, column=i%3, padx=10, pady=10)
            item_label = tk.Label(item_frame, text=item['name'], font=("Arial", 12), bg='white', fg=self.text_color)
            item_label.pack(pady=5)
            item_button = tk.Button(item_frame, text="View Details", font=("Arial", 10),
                                    command=lambda i=item: self.show_item_details(i, dining_hall))
            item_button.pack(pady=5)

    def show_item_details(self, item, dining_hall):
        details_window = tk.Toplevel(self.master)
        details_window.title(f"{item['name']} Details")
        details_window.geometry("300x200")
        details_window.configure(bg=self.bg_color)
        
        name_label = tk.Label(details_window, text=item['name'], font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color)
        name_label.pack(pady=10)
        
        nutrition_label = tk.Label(details_window, text=item['nutrition'], font=("Arial", 12), bg=self.bg_color, fg=self.text_color)
        nutrition_label.pack(pady=10)
        
        add_to_cart_button = tk.Button(details_window, text="Add to Cart", font=("Arial", 12),
                                       command=lambda: self.add_to_cart(item, dining_hall, details_window))
        add_to_cart_button.pack(pady=10)

    def add_to_cart(self, item, dining_hall, window):
        self.cart.append(f"{item['name']} from {dining_hall}")
        tk.Label(window, text="Added to cart!", font=("Arial", 12), bg=self.bg_color, fg='green').pack(pady=5)

    def open_cart(self):
        cart_window = tk.Toplevel(self.master)
        cart_window.title("Shopping Cart")
        cart_window.geometry("400x300")
        cart_window.configure(bg=self.bg_color)
        
        if self.cart:
            for item in self.cart:
                tk.Label(cart_window, text=item, font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=5)
        else:
            tk.Label(cart_window, text="Your cart is empty", font=("Arial", 14), bg=self.bg_color, fg=self.text_color).pack(pady=20)

    def open_calendar(self):
        calendar_window = tk.Toplevel(self.master)
        calendar_window.title("Calendar")
        calendar_window.geometry("300x300")
        calendar_window.configure(bg=self.bg_color)
        now = datetime.now()
        cal = calendar.monthcalendar(now.year, now.month)
        month_year_label = tk.Label(calendar_window, text=f"{calendar.month_name[now.month]} {now.year}", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        month_year_label.pack(pady=10)
        cal_frame = tk.Frame(calendar_window, bg=self.bg_color)
        cal_frame.pack()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day, font=("Arial", 10, "bold"), bg=self.bg_color, fg=self.text_color).grid(row=0, column=i, padx=5, pady=5)
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(cal_frame, text=str(day), width=4, height=2, command=lambda d=day: self.select_date(now.year, now.month, d), bg=self.bg_color, fg=self.text_color, bd=1, relief='solid')
                    btn.grid(row=week_num, column=day_num, padx=1, pady=1)

    def select_date(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        self.show_meals_for_date(date_str)

    def show_meals_for_date(self, date_str):
        meals_window = tk.Toplevel(self.master)
        meals_window.title(f"Meals on {date_str}")
        meals_window.geometry("300x200")
        meals_window.configure(bg=self.bg_color)
        if date_str in self.meals:
            for meal in self.meals[date_str]:
                tk.Label(meals_window, text=meal, font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=5)
        else:
            tk.Label(meals_window, text="No meals recorded for this date", font=("Arial", 12), bg=self.bg_color, fg=self.text_color).pack(pady=20)

root = tk.Tk()
app = DiningHallApp(root)
root.mainloop()