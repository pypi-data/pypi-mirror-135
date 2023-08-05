Epoch converter Scraper is a python library to scrape epoch converter, using browser automation. 
It currently runs only on windows.

## Scrape Epoch Converter Data
* In this, we first import library, then we fetched data using simple function. 
* Replace **"3"** with **"your data"**.

```json
from epoch_converter_scraper import *
response=epoch.timestamp_converter(time_stamp="3")
```
### Response Data
```json
 "Column A@txt": "Assuming that this timestamp is in seconds:GMT: Thursday, January 13, 2022 4:49:47 AMYour time zone: Thursday, January 13, 2022 4:49:47 AM GMT+00:00Relative: 2 minutes ago"
```

#### Bot Studio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up with epoch converter and loads the data.

#### Installation
```sh
pip install epoch-converter-scraper
```

#### Import
```sh
from epoch_converter_scraper import *
```
#### Get Data from Epoch Converter
```sh
response=epoch_timestamp_converter(time_stamp="3")
data=response['body']
```

#### Run bot on cloud
You can run bot on [cloud](https://datakund.com/products/epoch-timestamp-converter?_pos=1&_sid=e0ccd2d20&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)


