from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.deriv.com")

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

print(driver)
