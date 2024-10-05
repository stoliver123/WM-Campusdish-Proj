from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time


def ret_df(input_url):
    # Set up Chrome options (optional)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser window)

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Navigate to the target URL
    url = input_url
    driver.get(url)

    # Wait for the page to fully load (if necessary)
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

    # Maximize the browser window to ensure all elements are visible
    driver.maximize_window()

    # Get the page source after JavaScript rendering
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the product titles before interacting
    titles = soup.find_all('span', {'class': 'sc-fjvvzt kQweEp HeaderItemNameLink'})
    item_names = [title.text for title in titles]

    # Locate all buttons and add only enabled buttons to the list
    enabled_buttons = []
    for button in driver.find_elements(By.CLASS_NAME, "HeaderItem"):
        if not button.get_attribute('disabled'):
            enabled_buttons.append(button)  # Only add enabled buttons

    # Create a filtered list of item names corresponding to enabled buttons using their indices
    filtered_item_names = [button.accessible_name for button in enabled_buttons]

    # Dictionary to store item names and their nutrition facts
    nutrition_data = {}

    # Iterate through enabled buttons and click them to access nested content
    for index, button in enumerate(enabled_buttons[:5]):  # Use enabled_buttons and filtered_item_names together
        try:
            # Scroll to the button (if it's not visible on the screen)
            driver.execute_script("arguments[0].scrollIntoView(true);", button)

            # Use JavaScript to click the button
            driver.execute_script("arguments[0].click();", button)

            # Wait until the modal with nutritional information appears and is fully loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ModalProductServingSize'))
            )

            # Ensure the content stabilizes before proceeding (give time for any dynamic content to load)
            time.sleep(1)  # Optional: Adjust this time based on the page load behavior

            # Get the updated page source after clicking the button
            html_after_click = driver.page_source
            soup_after_click = BeautifulSoup(html_after_click, 'html.parser')

            # Extract the "Serving Size" information
            serving_size_div = soup_after_click.find('div', {'class': 'ModalProductServingSize'})
            serving_size = serving_size_div.text.strip() if serving_size_div else "Serving Size not found"

            # Extract the nutritional information under the <ul> tag
            nutrition_list = soup_after_click.find('ul', {'class': 'NutritionCard'})
            nutrition_facts = {}

            if nutrition_list:
                # Iterate through each <li> item in the nutrition list
                nutrition_items = nutrition_list.find_all('li', {'data-nesting': '1'})
                for item in nutrition_items:
                    # Extract nutrient name and value using separate selectors
                    nutrient_name = item.contents[0].strip()  # Get the text before the <span> tag
                    nutrient_value = item.find('span').text.strip() if item.find('span') else ""
                    nutrition_facts[nutrient_name] = nutrient_value

                    # Check for nested <ul> elements for more detailed information
                    sublist = item.find('ul')
                    if sublist:
                        sub_items = sublist.find_all('li', {'data-nesting': '2'})
                        for sub_item in sub_items:
                            # Extract sub-level nutrient name and value
                            sub_nutrient_name = sub_item.contents[0].strip()
                            sub_nutrient_value = sub_item.find('span').text.strip() if sub_item.find('span') else ""
                            nutrition_facts[sub_nutrient_name] = sub_nutrient_value

                            # Check for further nested <ul> elements (e.g., added sugars)
                            sub_sublist = sub_item.find('ul')
                            if sub_sublist:
                                sub_sub_items = sub_sublist.find_all('li', {'data-nesting': '3'})
                                for sub_sub_item in sub_sub_items:
                                    # Extract sub-sub-level nutrient name and value
                                    sub_sub_nutrient_name = sub_sub_item.contents[0].strip()
                                    sub_sub_nutrient_value = sub_sub_item.find('span').text.strip() if sub_sub_item.find('span') else ""
                                    nutrition_facts[sub_sub_nutrient_name] = sub_sub_nutrient_value

            # Add serving size to the nutrition facts
            nutrition_facts["Serving Size"] = serving_size

            # Map item name to its nutrition facts using the filtered item name
            item_name = filtered_item_names[index]  # Use filtered_item_names instead of item_names
            nutrition_data[item_name] = nutrition_facts

        except Exception as e:
            print(f"Could not interact with button {index + 1}: {e}")
            time.sleep(2)  # Wait for a while before trying the next button

    # Close the browser
    driver.quit()

    # Print the nutrition data dictionary
    # print("Nutrition Data:", nutrition_data)
    df=pd.DataFrame.from_dict(nutrition_data, orient='index')
    
    return df

print(ret_df("https://williamandmary.campusdish.com/LocationsAndMenus/CommonsDiningHall"))
