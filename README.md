# Price scraper

Scrapy spider which gets prices form a web catalouge and saves them to an Excel file. 

Spider automatically logs in with provided credentials then iterates through the Excel file with parts numbers. It goes to the part’s web page by adding that part number at the end of basic web addres.

![1](https://cloud.githubusercontent.com/assets/20326862/26356345/b3cf917c-3fc3-11e7-99b5-866e601ab791.JPG)

###### An example view of a file with part numbers and columns to fill in. 

From each part web page, the spider takes a list price, our price which is price with discount and a part number. Everything goes into a spreadsheet, always to the same row as the part number. Additional part number is used only to check if the spider got into a proper page.  For every wrong part number, spiders returns an error message and passes empty cells. 

![2](https://cloud.githubusercontent.com/assets/20326862/26356928/9cfc292c-3fc5-11e7-95d1-627ba9269daa.JPG)

###### An example view of Excel file with all fileds filled in.


