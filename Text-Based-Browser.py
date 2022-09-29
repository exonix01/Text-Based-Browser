import os
import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    history = []

    def __init__(self, dir_path):
        self.dir = dir_path

    def print_page(self, url):
        short_url = url.split('.')[0][8:]
        if short_url in os.listdir(self.dir):
            with open(self.dir + '/' + short_url, 'r') as file:
                page = file.read()
        else:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            if not r:
                print('Error!')
                return

            soup = BeautifulSoup(r.content, 'html.parser')
            page_text = soup.find_all(['title', 'p', 'a', 'ul', 'ol', 'li'])
            page = ''
            for n, line in enumerate(page_text):
                if line.name == 'a':
                    line = line.text
                    line = Fore.BLUE + line
                else:
                    line = line.text
                if not line:
                    continue
                page += line + '\n'

            with open(self.dir + '/' + short_url, 'w') as file:
                file.write(page)
        print(page)

    def main(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                return
            elif user_input == 'back':
                try:
                    self.history.pop()
                    self.print_page(self.history[-1])
                except IndexError:
                    continue
            elif '.' not in user_input:
                print('Invalid URL')
            else:
                if 'https://' not in user_input:
                    user_input = 'https://' + user_input
                self.history.append(user_input)
                self.print_page(user_input)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()
    dir_path = args.dir
    dir_path = './' + dir_path

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    browser = Browser(dir_path)
    browser.main()


if __name__ == "__main__":
    main()
