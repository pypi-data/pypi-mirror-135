Down Detector Scraper is a python library to scrape down detector scraper, using browser automation. 
It currently runs only on windows.

## Scrape down detector
In this example we first import library, then we fetched data using simple function.
 

```sh
from down_detector_scraper import *
response=down.detector()
```

### Response Data
```json     
        "brand": "Telegram",
        "description": "@himashugupta So thank ful to u that first u down the telegram and than its working fine...  2022-01-18 01:43:19",
        "parameter1": "App",
        "parameter2": "Server Connection",
        "parameter3": "Website",
        "parameter1_issue": "36%",
        "parameter2_issue": "36%",
        "parameter3_issue": "19%"
```

#### Bot Studio
For this project, we implemented an automated browser that scrapes search results from Naukri.com. [Bot Studio](https://pypi.org/project/botstudio/) is needed for browser automation. As soon as we import the library in code, an automated browser will open up and it will opens down detector and scrapes the data from it.

### Installation

```sh
pip install down-detector-scraper
```

### Import
```sh
from down_detector_scraper import *
```

###  Get Down Detector Data
```sh
response=down.detector()
```


### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Run Bot on Cloud
You can run bot on [Cloud](https://datakund.com/products/down-detector-issue-scraper?_pos=1&_sid=4b4c4a7be&_ss=r).

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

