# Kraken Browser

## Overview
Runs a chromium browser in the background.
Class Browser() retrieves a webpage along with images and screenshots

## Features
Auto-proxy: rotates proxy automatically


## Input
- url: url of the webpage to retrieve

## Attributes
- url: url of the webpage
- html: html fo the webpage retrieved
- screenshot: image object (dict) of the screenshot file (viewport)
- screenshot_full: image object (dict) of the screenshot file (full page)
- image_files: path of the image files
- images: array of image objects of the image files
- image object keys: 
    - schema:url url of the webpage
    - schema:contenturl url of the image
    - temp:data binary data of the image


## How to use

`from kraken_browser import Browser`

`url = 'https://www.test.com`

`browser = Browser(url)`

`html = browser.html`

