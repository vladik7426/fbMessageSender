import os
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from utils import selenium_utils
from utils.database_types import TaskRow


def send_messages_with_image(links: tuple | list, task: TaskRow):
    driver = selenium_utils.get_driver()
    for link in links:
        # Locate driver to the link
        driver.get(link)

        while True:
            try:
                # Open text-area
                write_button_element = driver.find_element(By.CSS_SELECTOR, "div[class='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou "
                                                                            "x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr "
                                                                            "x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv "
                                                                            "x1a2a7pz x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw "
                                                                            "x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 x1n2onr6 "
                                                                            "xt7dq6l x1ba4aug x1y1aw1k xn6708d xwib8y2 x1ye3gou'")
                write_button_element.click()
                break
            except NoSuchElementException:
                sleep(1)

        while True:
            try:
                # Write message text and send the image
                text_area = driver.find_element(By.CSS_SELECTOR, "._5rpu[role=textbox]")

                text_area.send_keys(task.ad)

                if os.path.isfile(task.photo):
                    assets_element = driver.find_element(By.CSS_SELECTOR, "[class='x6s0dn4 x1jx94hy x1n2xptk xkbpzyx xdppsyt "
                                                                        "x1rr5fae x1lq5wgf xgqcy7u x30kzoy x9jhf4c xev17xk "
                                                                        "x9f619 x78zum5 x1qughib xktsk01 x1d52u69 x1y1aw1k "
                                                                        "x1sxyh0 xwib8y2 xurb0ha']")

                    image_input = assets_element.find_element(By.CSS_SELECTOR, "input")
                    image_input.send_keys(task.photo)

                break
            except NoSuchElementException:
                sleep(1)

        # Press submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "[class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s "
                                                             "x1qughib x1qjc9v5 xozqiw3 x1q0g3np x1pi30zi x1swvt13 "
                                                             "xyamay9 xcud41i x139jcc6 x4vbgl9 "
                                                             "x1rdy4ex']").find_element(By.CSS_SELECTOR,
                                                                                        '[role=button]')
        sleep(1)
        submit_button.click()

        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, "[class='x9f619 x1ja2u2z x1k90msu x6o7n8i x1qfuztq x10l6tqk "
                                                     "x17qophe x13vifvy x1hc1fzr x71s49j']")
                if str(submit_button.get_attribute('tabindex')) != '-1':
                    submit_button.click()
                sleep(1)
            except NoSuchElementException:
                break
