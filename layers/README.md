# Lambda Layers

This directory contains source code for Lambda functions

1. `getter/` - This directory contains code for lambda function for getting data from DynamoDB
2. `modules/` - This directory contains zip file for python modules which are required in `rpitracker` lambda function. The following modules were installed-
    1. `BeautifulSoup4`
    2. `html5lib`
    3. `python-telegram-bot`
    4. `httpx`
3. `rpitracker/` - This directory contains source code for lambda function which is responsible for scraping URLs
