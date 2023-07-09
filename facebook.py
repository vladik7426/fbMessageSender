from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import selenium_utils


def send_message_with_image(link: str, message: str, image_src: str):
    # Locate driver to the link
    driver = selenium_utils.get_driver()

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
            text_area.send_keys(message)

            assets_element = driver.find_element(By.CSS_SELECTOR, "[class='x6s0dn4 x1jx94hy x1n2xptk xkbpzyx xdppsyt "
                                                                "x1rr5fae x1lq5wgf xgqcy7u x30kzoy x9jhf4c xev17xk "
                                                                "x9f619 x78zum5 x1qughib xktsk01 x1d52u69 x1y1aw1k "
                                                                "x1sxyh0 xwib8y2 xurb0ha']")

            image_input = assets_element.find_element(By.CSS_SELECTOR, "input")
            image_input.send_keys(image_src)
            break
        except NoSuchElementException:
            sleep(1)

    # Press submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, "[class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w "
                                                         "xeuugli x1iyjqo2 xs83m0k x150jy0e x1e558r4 xjkvuk6 x1iorvi4"
                                                         " xdl72j9']").find_element(By.CSS_SELECTOR, '[role=button]')
    sleep(1)
    submit_button.click()
