import os
from time import sleep
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.database_types import TaskRow, FBGroupRow


def locate_write_button(driver):
    while True:
        try:
            write_button_element = driver.find_element(By.CSS_SELECTOR, "div[class^='x1i10hfl']")
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
            submit_button = driver.find_element(By.CSS_SELECTOR, "[class^='x9f619 x1ja2u2z x1k90msu']")
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
