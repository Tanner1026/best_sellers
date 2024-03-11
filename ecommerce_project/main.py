from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
from datetime import date
import time

#establish variables for your Amazon Account including Username and Password
URL = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
email = "YOUR EMAIL/PHONE NUMBER HERE"
password = 'YOUR PASSWORD HERE'
today = date.today()
# Creates class for handling Database functions
class Database:
    def __init__(self):
        self.con = sqlite3.connect("listings.db")
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS listings(
                         id INTEGER PRIMARY KEY,
                         listing_name TEXT,
                         price TEXT,
                         link TEXT,
                         date TEXT
        );''')
        self.con.commit() 
    
    def execute(self, obj_name, price, link, today):
        full_listing = '''INSERT INTO listings(listing_name, price, link, date) VALUES (?, ?, ?, ?);'''
        self.con.execute(full_listing, (obj_name, price, link, today))
        self.con.commit()

    def get_listing_by_id(self, id):
        select_listing_sql = '''
        SELECT * FROM listings
        WHERE id = ?;
        '''
        self.cur.execute(select_listing_sql, (id,))
        result = self.cur.fetchone()

        return result
    def close_connection(self):
        self.cur.close()
        self.con.close()

#Determine if user wants data logged or not
def log_data():
    database_entry = input('Would you like the information uploaded to your Database? (y/n) ')
    if database_entry == 'y':
        return True
    else:
        return False
    
user_input  = log_data()

#Initialize Selenium Webdriver as well as the Database class
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL)
db = Database()
db.create_table()
#Use this time.sleep to enter any Captcha (if applicable)
time.sleep(20)

#Navigation to Best Sellers page
username = driver.find_element(By.ID, 'ap_email')
username.send_keys(email)
username.send_keys(Keys.ENTER)
time.sleep(2)

password_entry = driver.find_element(By.ID, 'ap_password')
password_entry.send_keys(password)
password_entry.send_keys(Keys.ENTER)

#Captcha can be either before or after the login process so including a second time.sleep to account for either
time.sleep(20)

nav = driver.find_element(By.ID, 'nav-hamburger-menu')
nav.click()
time.sleep(2)

item_menu = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/ul[1]/li[2]/a')
item_menu.click()
time.sleep(3)

#Collect data from best sellers page and insert them into the Database
best_sellers = driver.find_elements(By.CLASS_NAME, 'a-carousel')
time.sleep(3)
for item in best_sellers:
    items = item.find_elements(By.CLASS_NAME, 'a-carousel-card')
    for listing in items:
        anchor_tag = listing.find_element(By.CSS_SELECTOR, 'a')
        href = anchor_tag.get_attribute('href')
        name = listing.find_element(By.CLASS_NAME, 'p13n-sc-truncate-desktop-type2').text
        price = listing.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z').text
        if user_input:
            db.execute(name, price, href, today)
        else:
            print(f'Item name is: {name}\nThe price is: {price}\nThe link is: {href}\n\n')
