from scrapy import Spider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from urllib.parse import urljoin
import sqlite3


class PricesSpider(Spider):
    name = 'prices'
    allowed_domains = ["mall.industry.siemens.com"]

    def start_requests(self):
        # 'login_url' is a page where spiders stars and logs in to get prices
        # 'absolute_part_url' is a generic url to access particular part web page,
        # a part number is added at the end of the url to do that
        login_url = 'http://mall.industry.siemens.com/regpublic/Login.aspx?regionkey=GB&lang=en&app=MALL&ret=https' \
                     '%3a%2f%2fmall.industry.siemens.com%2fgoos%2fWelcomePage.aspx%3fregionUrl%3d%252fuk&login=&pwd= '
        absolute_part_url = 'https://mall.industry.siemens.com/mall/en/uk/Catalog/Product/'

        # Chrome web driver opens login page(login_url), inserts a login and a password and then clicks the login button
        self.driver = webdriver.Chrome()
        self.driver.get(login_url)
        self.driver.find_element_by_id("ContentPlaceHolder1_TextSiemensLogin").send_keys('USER_LOGIN')
        self.driver.find_element_by_id("ContentPlaceHolder1_TextPassword").send_keys('USER_PASSWORD')
        self.driver.find_element_by_id("ContentPlaceHolder1_LoginUserNamePasswordButton").click()
        # 'sleep' have to be there, Selenium works too slow and code executes faster than Selenium refreshes
        # Seems like a typical problem as Selenium is not really crated for scrapping
        sleep(3)

        # SQLite connects to the DB
        con = sqlite3.connect('test.db')

        with con:
            cur = con.cursor()  # Setting up the cursor
            cur.execute("SELECT Part_no FROM Parts")    # Getting parts number from the part table
            parts = cur.fetchall()   # Creates list out of

            # Iterating through the parts number in the table
            for part in parts:
                # Creating a part specific url by adding the a number and the end of the absolute url
                # Variable 'part' is a tuple with a part number at [0] position
                part_url = urljoin(absolute_part_url, part[0])
                self.driver.get(part_url)

                try:
                    # Webdiver gets prices form a part web pages
                    # and then removes EUR symbols and thousands separators
                    price = self.driver.find_element_by_id("CustomerPriceCell").text.replace('EUR', '').replace('.', '')
                    list_price = self.driver.find_element_by_id("ListPriceCell").text.replace('EUR', '').replace('.', '')

                    # Updates the  table's row with new prices
                    cur.execute("UPDATE Parts SET Our_price=?, List_price=? WHERE Part_no=?",
                                (price, list_price, part[0]))
                    con.commit()

                # When a part number is wrong or there is no such part, 'error' will be inserted to the table
                except NoSuchElementException:
                    cur.execute("UPDATE Parts SET Our_price=?, List_price=? WHERE Part_no=?",
                                ('error', 'error', part[0]))
                    con.commit()

                yield Request(part_url, callback=self.parse_price)

    def parse_price(self, response):
        pass

# Pieces to use spider as a script
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PricesSpider)
    process.start()     # The script will block here until the crawling is finished
