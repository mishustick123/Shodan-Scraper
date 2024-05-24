from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from progress.bar import Bar
import os
import time

options = Options()
options.add_argument("--headless=new")

browser = webdriver.Chrome(options=options)

stealth(browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


part1_domain = 'https://www.shodan.io/search?query=Android+Debug+Bridge+Name%3A+country%3A'
part2_domain = input('Введите букавы региона: ')
os.system('cls' if os.name == 'nt' else 'clear')
final_domain = part1_domain + part2_domain

login_url = 'https://account.shodan.io/login'

txt_dump = open('K:\selenium\shodan\weatifulsoup\devices.txt', 'a')

def login():
    print('Произвожу вход в аккаунт!')
    browser.get('https://account.shodan.io/login?')
    browser.find_element(by=By.ID, value='username').send_keys('rcollins52')
    browser.find_element(by= By.ID, value='password').send_keys('Waffle@9880')
    press_enter_xpath = '/html/body/div[2]/main/div/div/div/div[1]/form/div[3]/input'
    browser.find_element(by=By.XPATH, value=press_enter_xpath).click()  
    print('Бот успешно зашёл в аккаунт!')
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def main(page_counter=1):
    login()     
    bar = Bar('Scraping', fill='#', suffix='%(percent)d%%')   
    for i in range(20):
        browser.get(f'{final_domain}&page={page_counter}')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        ips = soup.findAll('a', class_='title text-dark')
        for host in ips:
            href = host['href'].split('/')[-1]
            txt_dump.write(f'{href}\n')
        
        page_counter += 1
        bar.next(5)

if __name__ == "__main__" :
    main()