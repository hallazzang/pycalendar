# pycalendar
Python alternative to Unix cal

## What is it?
It is a tiny console script that can replace [Unix cal](https://en.wikipedia.org/wiki/Cal_(Unix)).
Unfortunately it only supports Korean now.

## Features
- More familiar date format
- Marks today and holidays

## Install
Clone this repository and install the script using `pip`:
```bash
$ git clone https://github.com/hallazzang/pycalendar
$ cd pycalendar
$ pip install .
```

Then you can run the script typing `pycal` in your terminal.

## Fetching Holidays
After installing the script, you may want to fetch holidays data using [SK T EventDay API](https://developers.sktelecom.com/content/product/view/?svcId=10072).
Surprisingly, I've hard-coded my API key in the script(knowing I SHOULD NOT do that). It has a limit of 10,000 queries per day, so if the number of users increases in the future I'll find some other ways.

You can fetch holidays data using `pycal-fetch`:
```bash
$ pycal-fetch # Fetch holidays in this year
$ pycal-fetch -y 2015 # Fetch holidays in 2015
```

## Screenshot
![Screenshot](https://i.imgur.com/ekbGFfn.png)
