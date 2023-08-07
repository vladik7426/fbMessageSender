import os
from time import sleep
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.database_types import TaskRow, FBGroupRow


def locate_write_button(driver):
    while True:
        try:
            write_button_element = driver.find_element(By.CSS_SELECTOR, "div[class^='x1i10hfl x6umtig x1b1mbwd "
                                                                        "xaqea5y xav7gou x9f619 x1ypdohk xe8uvvx "
                                                                        "xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 "
                                                                        "x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz "
                                                                        "x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw "
                                                                        "x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 "
                                                                        "x1n2onr6 xt7dq6l x1ba4aug x1y1aw1k xn6708d "
                                                                        "xwib8y2 x1ye3gou']")
            write_button_element.click()
            break
        except NoSuchElementException:
            sleep(1)

def write_message(driver, task):
    while True:
        try:
            text_area = driver.find_element(By.CSS_SELECTOR, "._5rpu[role=textbox]")
            text_area.send_keys(' ')

            data_text_span = text_area.find_element(By.CSS_SELECTOR, "span[data-text=true]")
            driver.execute_script(f'''
                const text = `{task.ad}`;
                const dataTransfer = new DataTransfer();
                dataTransfer.setData('text', text);
                const event = new ClipboardEvent('paste', {{
                    clipboardData: dataTransfer,
                    bubbles: true
                }});
                arguments[0].dispatchEvent(event)
            ''', data_text_span)

            if task.photo is not None and os.path.isfile(task.photo):
                assets_element = driver.find_element(By.CSS_SELECTOR, "[class^='x6s0dn4 x1jx94hy']")

                image_input = assets_element.find_element(By.CSS_SELECTOR, "input")
                image_input.send_keys(task.photo)

            break
        except NoSuchElementException:
            sleep(1)


def press_submit_button(driver):
    while True:
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "[class^='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s "
                                                                 "x1qughib x1qjc9v5 xozqiw3 x1q0g3np x1pi30zi "
                                                                 "x1swvt13 xyamay9 xcud41i x139jcc6 x4vbgl9 "
                                                                 "x1rdy4ex'] [class^='x1i10hfl xjbqb8w x6umtig "
                                                                 "x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r "
                                                                 "x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 "
                                                                 "xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd "
                                                                 "x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 "
                                                                 "x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3']")
            submit_button.click()
            sleep(1)
        except NoSuchElementException:
            break


def send_ad_to_group(driver, fb_group: FBGroupRow, task: TaskRow):
    driver.get(fb_group.url)
    locate_write_button(driver)
    write_message(driver, task)
    press_submit_button(driver)

# Example usage
# send_ad_to_group(driver, fb_group_row, task_row)
