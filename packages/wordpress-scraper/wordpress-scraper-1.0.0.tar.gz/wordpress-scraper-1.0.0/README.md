WordPress Scraper is a python library to scrape blog data from WordPress blog, using browser automation. 
It currently runs only on windows.

## Scrape Blog details
* In this, we first import library to scrape.
```sh
from wordpress_scraper import *
response = wordpress.blog()
```

### Response Data

```json
        "post": "Get Started with new\u00a0webinars",
        "post_link": "https://wordpress.com/blog/2022/01/07/get-started-with-new-webinars/",
        "description": "Launching a website or learning how to monetize your online store can be overwhelming. But we are here to help you along the way. We are hosting free webinars to help get you on track and answer any questions you have.\u00a0 We cover different topics and will soon have new \u2026",
        "post_by": "Carla Doria",
        "date": "January 7, 2022"
```
#### Bot Studio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which, WordPress blog page opens and data is scraped from the page.


### Installation

```sh
pip install wordpress-scraper
```

### Import
```sh
from wordpress_scraper import *
```

### Get blog data
```sh
wordpress.blog()
```

### Run bot on cloud
You can run bot on [Cloud](https://datakund.com/products/wordpress-blog?_pos=4&_sid=09593a384&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)




