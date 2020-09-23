from selenium.webdriver.chrome.options import Options
options = Options()

options.add_argument("--headless")
options.add_argument("window-size=1400,1500")

def getChromeCustomOptions():
    return options