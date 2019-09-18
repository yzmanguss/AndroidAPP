from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

def search():
    browser.get("http://www.zhihu.com")
    #等待加载---判断是否成功
    change = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > div > div > div.SignContainer-inner > div.SignContainer-switch > span")))
    change.click()
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.SignFlow-account > div.SignFlowInput.SignFlow-accountInputContainer > div.SignFlow-accountInput.Input-wrapper > input")))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > div.SignFlow-password > div > div.Input-wrapper > input")))
    login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > div > div > div.SignContainer-inner > div.Login-content > form > button")))
    username.send_keys("Anguss")
    password.send_keys("y1720584431")

    login.click()

def main():
    search()


if __name__ =="__main__":
    main()