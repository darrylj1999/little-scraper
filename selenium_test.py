from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = "https://www.salesgenie.com/sign-in/"

# Launch Chrome 74
driver = webdriver.Chrome(executable_path='/Users/darryl/Documents/RESEARCH/scrape_auth/chromedriver')

# Go to Website
driver.get(url)
assert "salesgenie" in driver.page_source

# Input Username and Password
elem = driver.find_element_by_name("")
driver.implicitly_wait(5)
elem = driver.find_element_by_name("UserName")
elem.clear()
elem.send_keys("jacobchdr@gmail.com")
elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys("molly1962")
elem.send_keys(Keys.RETURN)

elem = driver.find_element_by_xpath("//*")
source_code = elem.get_attribute("outerHTML")
f = open('html_source_code.html', 'w')
f.write(source_code.encode('utf-8'))
f.close()

driver.close()
