from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--no-sandbox");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

def getChromeCustomOptions():
    return options
