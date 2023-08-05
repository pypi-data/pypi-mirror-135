Wikipedia scraper is a python library to scrape for a Wikipedia. using browser automation. 
It currently runs only on windows.

## Scrape Wikipedia Current events
 In this, we first import library, then we provide the keywords.


```sh
from wikipedia_scraper_in import *
response = wikipedia.current_events()
```

### Response Data
```sh
        "title": "An apartment fire",
        "description": "An apartment fire in the Bronx, New York City, kills 17 people.",
        "link": "/wiki/2022_Bronx_apartment_fire"
```
 
### Bot Studio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. When this library is imported in code, an automated browser will automatically open up in which it open wikipedia page and scrapes data from the page.

### Installation
```sh
pip install wikipedia-scraper-in
```

### Import
```sh
from wikipedia_scraper_in import *
```

### Get Current Events 
```sh
response = wikipedia.current_events()
data=response['body']
```

### Run bot on cloud
You can run bot on [Cloud](https://datakund.com/products/wikipedia-current-events?_pos=1&_sid=14f41b6c0&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

