import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# channel = input('enter channel videos url: ')
# channel = channel.split("/")
# channel = channel[0] + "//" + channel[2] + "/" + channel[3] + "/" + channel[4]

# print(channel)

# browser = webdriver.Safari()
# browser = webdriver.Firefox()

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

executable_path=os.environ.get("CHROMEDRIVER_PATH")

browser = webdriver.Chrome(options=options)


class Suggestion:
    def __init__(self, url, category, tags, id):
        self.url = url
        self.category = category
        self.tags = tags
        self.id = id


try:
    browser.get(f"https://www.showcasingcreators.com/suggest-channel/admin/show?admin={os.environ.get('ADMIN')}")

    ids = browser.find_elements_by_css_selector("button.btn.btn-outline-danger")
    urls = browser.find_elements_by_css_selector(".url")
    categories = browser.find_elements_by_css_selector(".category")
    tags = browser.find_elements_by_css_selector(".tags")

    idsArray = []
    urlArray = []
    categoryArray = []
    tagsArray = []

    for eachIds in ids:
        # print(eachIds.get_attribute("id"))
        idsArray.append(eachIds.get_attribute("id"))

    for eachUrl in urls:
        # print(eachUrl.text)
        # eachUrl = eachUrl.text.split("/")
        # eachUrl = eachUrl[0] + "//" + eachUrl[2] + "/" + eachUrl[3] + "/" + eachUrl[4]
        urlArray.append(eachUrl.text)
    for eachCategory in categories:
        # print(eachCategory.text)
        categoryArray.append(eachCategory.text)
    for eachTags in tags:
        # print(eachTags.text)
        tagsArray.append(eachTags.text)
    
    print(idsArray)
    print(urlArray)
    print(categoryArray)
    print(tagsArray)

    suggestionObjects = []

    for index, url in enumerate(urlArray):
        item = Suggestion(url, categoryArray[index], tagsArray[index], idsArray[index])
        suggestionObjects.append(item)

    for suggestion in suggestionObjects:
        try:
            print("-----------------------------------------------------------------------")
            print(suggestion.url, suggestion.category, suggestion.tags)

            browser.get(suggestion.url)

            channelName = browser.find_element_by_css_selector(
                ".ytd-channel-name > #text").text
            print(channelName)

            image = browser.find_element_by_css_selector(
                "#avatar>#img").get_attribute("src")
            print(image)

            browser.get(suggestion.url+"/about")
            description = browser.find_element_by_css_selector(
                "#description.style-scope.ytd-channel-about-metadata-renderer").text
            print(description)

            browser.get(f"https://www.showcasingcreators.com/suggest-channel/admin?admin={os.environ.get('ADMIN')}")

            # time.sleep(3)
            # print(browser.page_source)

            print("input description")
            inputDescription = browser.find_element_by_id("channelDescription")
            inputDescription.clear()
            inputDescription.send_keys(description)

            print("channel url")
            inputUrl = browser.find_element_by_id("channelUrl")
            inputUrl.clear()
            inputUrl.send_keys(suggestion.url)

            print("input name")
            inputName = browser.find_element_by_id("channelName")
            inputName.clear()
            inputName.send_keys(channelName)

            print("input image")
            inputImg = browser.find_element_by_id("channelImg")
            inputImg.clear()
            inputImg.send_keys(image)

            
            print("input category")
            inputTags = browser.find_element_by_id("channelTags")
            inputTags.location_once_scrolled_into_view
            inputTags.clear()
            inputTags.send_keys(suggestion.category, ", ", suggestion.tags)

            print("input password")
            inputPassword = browser.find_element_by_id("admin")
            inputPassword.clear()
            inputPassword.send_keys(f"{os.environ.get('ADMIN')}")

            browser.find_element_by_id("saveChannel").click()

            print("channel saved")

            browser.get(f"https://www.showcasingcreators.com/suggest-channel/admin/show?admin={os.environ.get('ADMIN')}")

            # time.sleep(3)
            print("deleting suggestion...")
            browser.find_element_by_id("admin-password").send_keys(f"{os.environ.get('ADMIN')}")
            browser.find_element_by_id(suggestion.id).click()
            browser.find_element_by_id("admin-password").clear()

            print("suggestion deleted")
        
        except Exception as e:
            print(e)
            continue

    browser.quit()

except Exception as e:
    print(e)
    browser.quit()
