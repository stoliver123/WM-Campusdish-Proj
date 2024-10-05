from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

# Iterate through each button and click it to access nested content
# Example of re-finding the element inside the loop
for index, _ in enumerate(buttons):
    try:
        # Re-find the button to avoid stale reference
        buttons = driver.find_elements(By.CLASS_NAME, "HeaderItem")
        button = buttons[index]
        
        # Scroll to and click the button using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
        
        # Wait for nested content to load (if necessary)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ItemInfo')))
        
        # Get updated content after interaction
        html_after_click = driver.page_source
        soup_after_click = BeautifulSoup(html_after_click, 'html.parser')

        # Extract desired information
        product_info = soup_after_click.find('div', {'class': 'ItemInfo'})
        if product_info:
            calories = product_info.find('span', {'data-testid': 'product-card-info-block-calories'})
            description = product_info.find('p', {'data-testid': 'product-card-description'})

            if calories:
                print("Calories:", calories.text)
            if description:
                print("Description:", description.text)

        # Sleep for 2 seconds before the next interaction
        time.sleep(2)

    except Exception as e:
        print(f"Could not interact with button: {e}")


# Close the browser
driver.quit()
