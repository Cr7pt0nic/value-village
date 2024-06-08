# Installation guide:

## Install chromedriver
https://developer.chrome.com/docs/chromedriver/downloads

Create a directory called "chromedrive" within the same directory as the "automate.py" script.
Next place the chromedriver in the "chromedrive" folder.

Next execute these commands.
install required modules
```
pip install -r requirements.txt
```

change and modify the config file to include zipcode and email

```
{
    "zipcode": "ZIPCODE HERE",
    "email": "EMAIL HERE"
}
```

run the script
```
python3 automate.py
```
