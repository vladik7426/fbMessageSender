from threading import Thread

import database
import facebook


def send_ad(facebook_links, text, title, photo):
    for link in facebook_links:
        facebook.send_message_with_image(link, text, photo)


def main():
    links = (row[2] for row in database.get_facebook_group_rows())
    while True:
        tasks = database.get_task_rows()
        for task in tasks:
            if task[2] != 'DONE':
                Thread(target=send_ad, args=(links, task[1], task[6], task[5],)).start()
                break


if __name__ == '__main__':
    main()
