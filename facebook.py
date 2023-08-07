import os
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from utils.database_types import TaskRow, FBGroupRow


def send_ad_to_group(driver, fb_group: FBGroupRow, task: TaskRow):
    # Locate driver to the link
    driver.get(fb_group.url)

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
            js_set_text_in_elem = """
              var elm = arguments[0], txt = arguments[1];
              elm.textContent = txt
              """

            text_area = driver.find_element(By.CSS_SELECTOR, "._5rpu[role=textbox]")
            text_area.send_keys(' ')

            data_text_span = text_area.find_element(By.CSS_SELECTOR, "span[data-text=true]")
            driver.execute_script(js_set_text_in_elem, data_text_span, task.ad)

            if task.photo is not None and os.path.isfile(task.photo):
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
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, "[class='x9f619 x1ja2u2z x1k90msu x6o7n8i x1qfuztq x10l6tqk "
                                                 "x17qophe x13vifvy x1hc1fzr x71s49j']")
            driver.execute_script("document.querySelector('input[type=submit]').click()")
            sleep(1)
        except NoSuchElementException:
            break
