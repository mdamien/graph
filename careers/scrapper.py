from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.google.com/about/careers/search#t=sq&q=j&so=dt_d&li=10&st=1800&")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'kd-count')))


#click first link
driver.find_element_by_css_selector('.title.heading.sr-title').click()

#save page by page
i = 2500
while True:
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'kd-count')))
    print(i,driver.title)
    with open('PAGES/%d.html' % i,'w') as f:
        f.write(driver.page_source)
    driver.find_element_by_css_selector('.kd-button.right.small').click()
    i += 1


driver.close()
