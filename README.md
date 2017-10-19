# Siemens Mall Price Scrapper

Small stand alone crawler script. Made to make my life easier, it goes through part numbers in a db and then goes to that parts pages and gets its prices.  

### How to use

Download both files. Start with *db_seed.py*, fill in part numbers you want to get prices for and then run the file. Then in *prices.py* insert your Siemens Mall credentials where `USER_LOGIN` and `USER_PASSWORD` are.

Check locations of your Selenium Webdiver and SQLite files and change the code if needed.

Spider automatically logs in with provided credentials then iterates through the db. Two prices are taken, one is a list price for the item and second is a price with your company discount. If the webpage for the given part is non existent or there is no prices for some reason, script inserts error message to the table.

Below you can find example table with two prices scrapped and one wrong part number and error notification.

| Part number        | Discounted Price | List Price  |
| ------------------ | :--------------: | :---------: |
| 6ES7215-1HF40-0XB0 | 753.45           |  984.34     |
| 6ES7414-3XM07-0AB1 | error            |  error      |
| 6ES7221-1BF32-0XB0 | 72.94            |  96.90      |

### Technologies used
* Scrapy
* Selenium
* SQLite3
