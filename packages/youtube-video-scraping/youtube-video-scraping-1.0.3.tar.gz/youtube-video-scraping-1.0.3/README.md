Youtube Video Scraping is a python library to scrape youtube video data using browser automation. 
It currently runs only on windows.

## Youtube Video scraping 
In this, we first import library, then we fetched data using simple function, and replace below **'youtube URL'**.
```sh
from youtube_video_scraping import *
response=youtube.get_video_info(video_url='https://www.youtube.com/watch?v=LMmuChXra_M')
data=response['body']

```

### Response Data
```json
{
 "DisLikes": "4.8K", 
 "Title": "OM Chanting @ 528Hz",
 "Subscribers": "3.66M",
 "Comments": "2631",
 "ChannelLink": "https://www.youtube.com/channel/UCM0YvsRfYfsniGAhjvYFOSA",
 "ChannelName": "Meditative Mind",
 "Desc": "OM is the mantra, or vibrations that is chanted in the beginning and end of any Meditation or Yoga ",
 "Views": "9,737,330 views",
 "Duration": "3:20:02",
 "Publish_Date": "17 Aug 2016",
 "Likes": "84K"
}
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)
 
 ## Youtube Comments scraping 
In this, we first import library, then we fetched data using simple function, and replace below **'youtube URL'**.

```sh
from youtube_video_scraping import *
response=youtube.comments(youtube_link='https://www.youtube.com/watch?v=LMmuChXra_M')
data=response['body']
```

### Response Data
```json
{
        "user": "runner",
        "Comment": "\uac1c\uadf8\ub9e8 \uac1c\uadf8\uc6b0\uba3c\uc911 \uc7ac\ubc0c\ub294\ub370 \ubd88\ud3b8\ud55c\uacbd\uc6b0\ub9ce\uc740\ub370 \ub3c4\uc5f0\ub204\ub098\ub294 \uc9c4\uc9dc \ud3b8\ud558\uac8c \uc7ac\ubc0c\ub2e4 \ub354\uc6b1 \ud765\ud558\uc2dc\uae38",
        "UserLink": "/channel/UCkUgmFJLNYvAtaEWi1pQG7A",
        "Likes": "91",
        "Time": "16\uc2dc\uac04 \uc804"
}
```
 
#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which video will be opened, and scrapes the data.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-video-scraping
```

### Import
```sh
from youtube_video_scraping import *
```

### Login with credentials
```sh
youtube.login(username="youtube username",password="youtube password")
```

### Login with cookies
```sh
youtube.login_cookie(cookies=list_of_cookies)
```

### Get video info
```sh
youtube.login(username="youtube username",password="youtube password")
response=youtube.get_video_info(video_url='video_url')
data=response['body']
```

### Get only limited data
```sh
youtube.login(username="youtube username",password="youtube password")
response=youtube.get_video_info(video_url='video_url',fields=['Subscribers'])
data=response['body']
data={"Subscribers":""}
```

### Get Youtube Comments
```sh
youtube.login(username="youtube username",password="youtube password")
response=youtube.comments(video_url='https://www.youtube.com/watch?v=LMmuChXra_M')
data=response['body']
```

#### Run bot on cloud
Youtube Video scraping - You can run bot on [cloud](https://datakund.com/products/youtube-video-url?_pos=10&_sid=8a6ed6504&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

