import time
from typing import Final, List

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

FACEBOOK_GROUP_LINK: Final[str] = "https://www.facebook.com/groups/810917113840125"
cookie_dicts: List[dict] = [
    {
        'name': 'c_user',
        'value': '100093921954323',
        'domain': '.facebook.com',
        'path': '/',
        'expires': int(time.time()) + 100000000,
        'httpOnly': True,
        'secure': True,
        'session': False,
        'sameSite': 'None',
        'sameParty': False,
        'sourceScheme': 'Secure',
        'sourcePort': 443
    },
    {
        'name': 'xs',
        'value': '3%3AnUkxAmLZLB63wg%3A2%3A1688063096%3A-1%3A-1%3A%3AAcVFlwNmSRX6GXkw9UunXYOjujL2M8Mgdq7SyBKuoQ',
        'domain': '.facebook.com',
        'path': '/',
        'expires': int(time.time()) + 100000000,
        'httpOnly': True,
        'secure': True,
        'session': False,
        'sameSite': 'None',
        'sameParty': False,
        'sourceScheme': 'Secure',
        'sourcePort': 443
    }
]


def send_message(driver, message):
    # Open text-area
    write_button_element = driver.find_element(By.CSS_SELECTOR, "div[class='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou "
                                                                "x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr "
                                                                "x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv "
                                                                "x1a2a7pz x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw "
                                                                "x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 x1n2onr6 "
                                                                "xt7dq6l x1ba4aug x1y1aw1k xn6708d xwib8y2 x1ye3gou'")
    write_button_element.click()

    while True:
        try:
            # Write message text
            text_area = driver.find_element(By.CSS_SELECTOR, "._5rpu[role=textbox]")
            text_area.send_keys(message)
            break
        except NoSuchElementException:
            time.sleep(1)

    # Press submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, "[class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w "
                                                         "xeuugli x1iyjqo2 xs83m0k x150jy0e x1e558r4 xjkvuk6 x1iorvi4"
                                                         " xdl72j9']").find_element(By.CSS_SELECTOR, '[role=button]')
    submit_button.click()


def main():
    driver = webdriver.Edge()

    driver.get(FACEBOOK_GROUP_LINK)

    for cookie_dict in cookie_dicts:
        driver.add_cookie(cookie_dict)

    driver.get(FACEBOOK_GROUP_LINK)

    while True:
        send_message(driver, input("Message: "))


if __name__ == '__main__':
    main()
