from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Chrome options (optional)
options = Options()
# options.add_argument("--headless=new")  # Run in headless mode (no browser window)

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Navigate to the website
# url = "https://williamandmary.campusdish.com/LocationsAndMenus/CommonsDiningHall"
url = "https://williamandmary.campusdish.com/LocationsAndMenus/FoodHallSadler"
driver.get(url)

# Wait for the dynamic content to load (if necessary)
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

# Get the page source after JavaScript rendering
html = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract data using BeautifulSoup
# Example: Extract all product titles
titles = soup.find_all('span', {'class': 'sc-fjvvzt kQweEp HeaderItemNameLink'})
for title in titles:
    print(title.text)

# Close the browser
driver.quit()
