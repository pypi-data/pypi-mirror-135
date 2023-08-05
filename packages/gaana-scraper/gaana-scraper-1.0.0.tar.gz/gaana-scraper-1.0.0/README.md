Gaana Scraper is a python library to scrape data from Gaana, using browser automation. 
It currently runs only on windows.

## Scrape playlist
* In this, we first import library to scrape
* Provide **"playlist URL"** instead of 
```sh
from gaana_scraper import *
response = gaana.playlist(playlist_link="https://gaana.com/playlist/gaana-dj-hindi-top-50-1")
```

### Response Data

```json
        "track": "Raataan Lambiyan",
        "track_link": "/song/raataan-lambiyan-from-shershaah",
        "artists": "Jubin Nautiyal",
        "album": "Shershaah",
        "duration": "03:50"
```
#### Bot Studio
[Bot_Studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which, gaana website will open and load the playlist link to scrape the data .


### Installation

```sh
pip install gaana-scraper
```

### Import
```sh
from gaana_scraper import *
```

### Get Playlist Data
```sh
gaana.playlist(playlist_link="https://gaana.com/playlist/gaana-dj-hindi-top-50-1")
```

### Run bot on cloud
You can run bot on [Cloud](https://datakund.com/products/gaana-scraper?_pos=1&_sid=c0391273b&_ss=r).

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

