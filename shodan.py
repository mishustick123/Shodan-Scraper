from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from progress.bar import Bar
import os
import time
import pycountry
from urllib import parse
import argparse

parser = argparse.ArgumentParser(description='The best shodan scraper!')
parser.add_argument(
                    '-q',
                    '--query',
                    type=str,
                    help='Ur query',
                    required=True)
parser.add_argument(
                    '--show',
                    type=bool,
                    help='Show process of scraping',
                    required=False)
parser.add_argument(
                    '-u',
                    '--username',
                    type=str,
                    help='Username',
                    required=True
)
parser.add_argument(
                    '-p',
                    '--password',
                    type=str,
                    help='Password',
                    required=True
)
parser.add_argument(
                    '-o',
                    '--output',
                    type=str,
                    help='Output',
                    required=True
)
args = parser.parse_args()

options = Options()
browser = webdriver.Chrome(options=options)
login_url = 'https://account.shodan.io/login'
txt_dump = open(args.output, 'a')

if args.show == False:
    options.add_argument("--headless=new")

stealth(browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

def login():
    print('Произвожу вход в аккаунт!')
    browser.get('https://account.shodan.io/login?')
    browser.find_element(by=By.ID, value='username').send_keys(args.username)
    browser.find_element(by= By.ID, value='password').send_keys(args.password)
    press_enter_xpath = '/html/body/div[2]/main/div/div/div/div[1]/form/div[3]/input'
    browser.find_element(by=By.XPATH, value=press_enter_xpath).click()  
    print('Бот успешно зашёл в аккаунт!')
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    login()     
    bar = Bar('Scraping', fill='#', suffix='%(percent)d%%')   
    for country in pycountry.countries:
        domain = f'https://www.shodan.io/search?query={parse.quote(args.query)}+country%3A'
        page_counter = 1
        for country in pycountry.countries:
            for i in range(20):
                code = country.alpha_2
                full_domain = domain + code
                browser.get(f'{full_domain}&page={page_counter}')
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                ips = soup.findAll('a', class_='title text-dark')
                for host in ips:
                    href = host['href'].split('/')[-1]
                    txt_dump.write(f'{href}\n')
                page_counter += 1
                if len(ips) == 0:
                    page_counter = 1
                    bar.next(100/len(pycountry.countries))
                    break    

if __name__ == "__main__" :
    main()
