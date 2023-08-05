LinkedIn search results is a python library to scrape LinkedIn search results, using browser automation. 
It currently runs only on windows.

### LinkedIn login with Credentials
We first import library. Replace **"email"** and **"password"** with your credentials to login.
```sh
from linkedin_scraper_in import *
linkedin.login(email="email",password="password")
```

### LinkedIn login with Cookies 
We first import library. Replace **"cookies"** with login cookies.
```sh
from linkedin_scraper_in import *
linkedin.login_cookies(cookies="cookies")
```

### LinkedIn search results scraper
We first import library, then we provide the keyword instead of **"keyword"**, to scrape LinkedIn search results.
```sh
from linkedin_scraper_in import *
response=linkedin.search_results(keyword="keyword")
```
### Response Data
```json
       "title": "Adwords IndiaView Adwords India\u2019s profile",
       "position": "Adwords Coupon at Google Ads",
       "link": "https://www.linkedin.com/in/adwordsindia?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACvkQm8BiUuA9BgIlufcCW1I678EGwE77yg",
       "location": "Delhi, India"
```

### Scrape LinkedIn Learning 
We first import library, then we provide the keyword to be scraped instead of **"keyword"**. 
```sh
from linkedin_scraper_in import *
response=  
linkedin.learning_keyword(keyword="keyword")
```

### Response Data
```json
        "course": "Excel Essential Training (Office 365/Microsoft 365)",
        "instructor": "By: Dennis Taylor",
        "viewers": "1,222,352 viewers",
        "date": "Released Sep 24, 2018",
        "course_time": "2h 17m",
        "course_link": "https://www.linkedin.com/learning/excel-essential-training-office-365-microsoft-365?trk=learning-serp_learning-search-card_search-card&upsellOrderOrigin=default_guest_learning"
```

#### Bot Studio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up, logs in and then scrapes the search results based on the keyword given.


### Installation

```sh
pip install linkedin-scraper-in
```

### Import
```sh
from linkedin_scraper_in import *
```

### Get LinkedIn Data by logging in with Credentials 
```sh
linkedin.login(email="email",password="password")
response = linkedin.search_results(keyword="keyword")
```

### Get LinkedIn Data by logging in with Cookies
```sh
linkedin.login_cookies(cookies="cookies")
response = linkedin.search_results(keyword="keyword")
```
### Get LinkedIn Courses 
```sh
linkedin.login_cookies(cookies="cookies")
response = linkedin.learning_keyword(keyword="keyword")
```

### Cookies
To login with cookies [Edit this Cookie Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) can be added to browser. Please check [this](https://abhishek-chaudhary.medium.com/how-to-get-cookies-of-any-website-from-browser-22b3d6348ed2) link how to get cookies to login to your amazon.

### Run bot on Cloud
* LinkedIn search results - You can run bot on [Cloud](https://datakund.com/products/linkedin-profile-results-scraper).
* LinkedIn Learning - You can run bot on [Cloud](https://datakund.com/products/linkedin-learning-course-search?_pos=1&_sid=677534c5e&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

