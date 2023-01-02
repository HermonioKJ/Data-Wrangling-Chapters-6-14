from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()

browser.get('file:///C:/Users/USER/Documents/Projects/Python/Data Wrangling/Data Wrangling/data/chp11/twine_social_fairphone.html')
browser.maximize_window()

content = browser.find_element(by=By.CSS_SELECTOR, value='div.content')

print('\n\nCONTENT\n', content.text)

all_bubbles = browser.find_elements(by=By.CSS_SELECTOR, value='div.content')

print('\n\nLEN\n', len(all_bubbles))

for bubble in all_bubbles:
    print(bubble.text)

iframe = browser.find_element(By.XPATH, '//iframe')
new_url = iframe.get_attribute('src')
browser.get(new_url)

##

all_bubbles = browser.find_elements(By.CSS_SELECTOR, 'div.content')

for elem in all_bubbles:
    print(elem.text)

#

all_data = []
for elem in all_bubbles:
    elem_dict = {}
    elem_dict['full_name'] = \
        elem.find_element(By.CSS_SELECTOR, 'div.fullname').text
    elem_dict['short_name'] = \
        elem.find_element(By.CSS_SELECTOR, 'div.name').text
    elem_dict['text_content'] = \
        elem.find_element(By.CSS_SELECTOR, 'div.twine-description').text
    elem_dict['timestamp'] = elem.find_element(
        By.CSS_SELECTOR, 'div.when').text
    elem_dict['original_link'] = \
        elem.find_element(By.CSS_SELECTOR, 'div.when a').get_attribute('href')
    try:
        elem_dict['picture'] = elem.find_element(
            By.CSS_SELECTOR, 'div.picture img').get_attribute('src')
    except NoSuchElementException as E:
        elem_dict['picture'] = None
        print(E)
    all_data.append(elem_dict)

all_bubbles = browser.find_elements(By.CSS_SELECTOR, 'div.twine-item-border')
###


all_data = []
all_bubbles = browser.find_elements(By.CSS_SELECTOR,
                                    'div.twine-item-border')
for elem in all_bubbles:
    elem_dict = {'full_name': None,
                 'short_name': None,
                 'text_content': None,
                 'picture': None,
                 'timestamp': None,
                 'original_link': None,
                 }
    content = elem.find_element(By.CSS_SELECTOR, 'div.content')
    try:
        elem_dict['full_name'] = \
            content.find_element(By.CSS_SELECTOR, 'div.fullname').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['short_name'] = \
            content.find_element(By.CSS_SELECTOR, 'div.name').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['text_content'] = \
            content.find_element(By.CSS_SELECTOR, 'div.twine-description').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['timestamp'] = elem.find_element(By.CSS_SELECTOR,
                                                   'div.when').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['original_link'] = \
            elem.find_element(By.CSS_SELECTOR,
                              'div.when a').get_attribute('href')
    except NoSuchElementException:
        pass
    try:
        elem_dict['picture'] = elem.find_element(By.CSS_SELECTOR,
                                                 'div.picture img').get_attribute('src')
    except NoSuchElementException:
        pass
    all_data.append(elem_dict)
print(all_data)
