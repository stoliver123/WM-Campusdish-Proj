from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options (optional)
options = Options()
# Uncomment the line below to run the browser in headless mode (no GUI)
# options.add_argument("--headless")

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Navigate to the target URL
url = "https://williamandmary.campusdish.com/LocationsAndMenus/FoodHallSadler"
driver.get(url)

# Wait for the page to fully load (if necessary)
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

# Maximize the browser window to ensure all elements are visible
driver.maximize_window()

# Get the page source after JavaScript rendering
html = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract and print the product titles before interacting
titles = soup.find_all('span', {'class': 'sc-fjvvzt kQweEp HeaderItemNameLink'})
print("Before Clicking Buttons:")
for title in titles:
    print(title.text)

# Locate all buttons using their class or any unique attribute (modify as needed)
buttons = driver.find_elements(By.CLASS_NAME, "HeaderItem")

# Use a set to track unique food items to prevent duplicates
seen_food_items = set()

# Iterate through each button and click it to access nested content
for index, button in enumerate(buttons):
    try:
        # Scroll to the button (if it's not visible on the screen)
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        # Use JavaScript to click the button
        driver.execute_script("arguments[0].click();", button)

        # Wait for nested content to load (if necessary)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ModalProductServingSize')))

        # Get the updated page source after clicking the button
        html_after_click = driver.page_source
        soup_after_click = BeautifulSoup(html_after_click, 'html.parser')

        # Extract the "Serving Size" information
        food_item = soup_after_click.find('h2', {'class': 'sc-krNlru jTWVjC ModalHeaderItemName'})
        serving_size_div = soup_after_click.find('div', {'class': 'ModalProductServingSize'})
        serving_size = serving_size_div.text.strip() if serving_size_div else "Serving Size not found"
        
        if food_item:
            food_item_name = food_item.text.strip()
            # Check if this food item has already been processed
            if food_item_name not in seen_food_items:
                seen_food_items.add(food_item_name)  # Add to the set to avoid duplicates
                print(f"Item: {food_item_name}: Serving Size: {serving_size}")
            else:
                print(f"Item '{food_item_name}' has already been processed. Skipping.")
        else:
            print(f"Item {index + 1}: Food item not found.")

        # Extract the nutritional information under the <ul> tag
        nutrition_list = soup_after_click.find('ul', {'class': 'NutritionCard'})
        if nutrition_list:
            # Iterate through each <li> item in the nutrition list
            print(f"Item {index + 1} Nutrition Facts:")
            nutrition_items = nutrition_list.find_all('li', {'data-nesting': '1'})
            for item in nutrition_items:
                # Extract nutrient name and value using separate selectors
                nutrient_name = item.contents[0].strip()  # Get the text before the <span> tag
                nutrient_value = item.find('span').text.strip() if item.find('span') else ""

                print(f"  {nutrient_name}: {nutrient_value}")

                # Check for nested <ul> elements for more detailed information
                sublist = item.find('ul')
                if sublist:
                    sub_items = sublist.find_all('li', {'data-nesting': '2'})
                    for sub_item in sub_items:
                        # Extract sub-level nutrient name and value
                        sub_nutrient_name = sub_item.contents[0].strip()
                        sub_nutrient_value = sub_item.find('span').text.strip() if sub_item.find('span') else ""
                        print(f"    {sub_nutrient_name}: {sub_nutrient_value}")

                        # Check for further nested <ul> elements (e.g., added sugars)
                        sub_sublist = sub_item.find('ul')
                        if sub_sublist:
                            sub_sub_items = sub_sublist.find_all('li', {'data-nesting': '3'})
                            for sub_sub_item in sub_sub_items:
                                # Extract sub-sub-level nutrient name and value
                                sub_sub_nutrient_name = sub_sub_item.contents[0].strip()
                                sub_sub_nutrient_value = sub_sub_item.find('span').text.strip() if sub_sub_item.find('span') else ""
                                print(f"      {sub_sub_nutrient_name}: {sub_sub_nutrient_value}")

        # Close the modal after getting the information (if necessary)
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ModalCloseButton')))
        driver.execute_script("arguments[0].click();", close_button)

    except Exception as e:
        print(f"Could not interact with button: {e}")
        time.sleep(2)  # Wait for a while before trying the next button

# Close the browser
driver.quit()