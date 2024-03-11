# best_sellers
This is a project meant to be an asset to sellers/ecommerce resellers to find the most popular items on amazon and commit them to a database
A few things to note:
This is a selenium based project and so a few things could cause an error in the project including amazon changing class names, id names etc.  
In the beginning process of the driver displaying the webpage, there may be CAPTCHA requests.  This cannot be handled by Selenium and so there is a time.sleep counter to manually enter captcha
In order to use the Database function, you will need SQLite as that is what was used for tracking the data.  If you do not have SQLite, please select no for recording in Database
