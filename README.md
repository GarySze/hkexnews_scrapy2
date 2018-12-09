This project is based on: https://github.com/KennethYCK/hkexnews_scrapy and with the same functionliaty except:

* Implementation: Use Scrapy FormRequest instead of Selenium + ChromeDriver to hanle ASPX 
* Implementation: No Mango DB support
* Functionality: Support HKEx web page changed in late Oct2018
* Command line to run the scrapy is 
   ```python
  scacpy runspider instead of scrapy crawl 
   ```

Please refer to https://github.com/KennethYCK/hkexnews_scrapy for more detail.
