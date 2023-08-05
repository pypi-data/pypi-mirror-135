import asyncio
from pyppeteer import launch
import time
import requests
from fp.fp import FreeProxy
import os
import uuid


global loop
loop = None
TEMP_DIR = 'temp_images'


# Delete temp dir
import shutil


try:
    shutil.rmtree(TEMP_DIR)
except OSError as e:
    print("Error: %s : %s" % (TEMP_DIR, e.strerror))



class Browser:
    """Pyppeteer browser runnning extractions from website
    
    Args:
        url (str): The url of the webpage to retrieve
    Attributes:
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

    Methods:
        scrape(url)
        scrape_async(url)
    """

    def __init__(self, url = None):
        a=1

        # input
        self.url = url

        self.browser = browser

        # Processing
        self.page = None
        

        self.screenshot = None
        self.screenshot_full = None
        self.images = []    # Keeps images

        # Results

        self.html = None   

        self.status = False



    """
    API
    """


    def scrape(self, url):
        """Navigate pyppeteer to webopage and retrieves data
        
        Notes:

        Args:
            url (str): url fo the webpage to retrieve

        Returns:
            True if successful, else False
        
        """
        self.url = url
        
        
        try:
            loop.run_until_complete(self._run_scrape())

        except Exception as e:
            print(e)

        return 


    async def scrape_async(self, url):
        """
        Scrape webpage async
        """

        self.url = url
        return await self._run_scrape()


    """
    Methods
    """



    async def _run_scrape(self, url = None):

        """
        Scrape webpage, get screenshots, get image files
        """


        if url:
            self.url = url

        count_proxy = 0
        i = 0
        # Get page and process request, response
        while i < 8:
            try:
                await self._get_page()
                break
            except Exception as e:


                # Change proxy
        
                if count_proxy > 25:
                    return False

                await self.browser.close()
                self.browser = await pylaunch()
                print('Changing proxy')
                count_proxy += 1


                


        # Ensure page is loaded 
        print('load page')
        await self._lazy_loading()

        # Get screenshot 
        print('screenshots')

        await self._get_screenshot(1200, 800)
        await self._get_screenshot_full()

        # Retrieve html
        await self._get_html()


        self.status = True
        await self.page.close()

        return True



    async def _get_page(self):
        """Retrieves web page and runs response processor
        """
        i = 0
        while 1==1:
            try:
                self.page = await self.browser.newPage()
                break
            except:

                time.sleep(3)
                i+= 1
                if i > 15:
                    return


        await self.page.setViewport({'width': 1200, 'height': 800})
        await self.page.goto(self.url,  {'waitUntil' : 'networkidle0'})
        self.page.on('response', lambda response: asyncio.ensure_future(self._response_processor(response)))
        return


    async def _lazy_loading(self):
        """Scrols through entire doc to lazy load everything
        """
        viewportH = 800
        i = viewportH
        documentH = await self.page.evaluate("""{document.body.scrollHeight}""")

        while i < documentH:
            await self.page.evaluate('_i => {window.scrollBy(0, _i);}', i)
            i += viewportH
            time.sleep(0.5)
            

        return

    async def _get_screenshot(self, width = 1200, height = None):
        """Takes screenshot
        """

        # If not height, takes entire height of the doc
        if not height:
            height = await self.page.evaluate("""{document.body.scrollHeight}""")

        await self.page.setViewport({'width': width, 'height': height})

        # Build filename
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            a=1

        file_path = TEMP_DIR + '/' + str(uuid.uuid4()) + '.png'

        # Save screenshot to file
        #await self.page.screenshot({'path': file_path, 'fullPage': True})
        await self.page.screenshot({'path': file_path})

        
        image = {
            '@type': 'schema:ImageObject',
            'schema:url': self.url
        }

        # Load file to memory
        try:
            file = open(file_path, "rb")
            image['temp:data'] = file.read()
        except:
            a=1

        self.screenshot = image

        return


    async def _get_screenshot_full(self, width = 1200, height = None):
        """Takes screenshot
        """

# If not height, takes entire height of the doc
        if not height:
            height = await self.page.evaluate("""{document.body.scrollHeight}""")

        await self.page.setViewport({'width': width, 'height': height})

        # Build filename
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            a=1

        file_path = TEMP_DIR + '/' + str(uuid.uuid4()) + '.png'

        # Save screenshot to file
        await self.page.screenshot({'path': file_path, 'fullPage': True})
        #await self.page.screenshot({'path': file_path})

        
        # Load file to memory
        image = {
            '@type': 'schema:ImageObject',
            'schema:url': self.url
        }


        try:
            file = open(file_path, "rb")
            image['temp:data'] = file.read()
        except:
            a=1

        self.screenshot = image


        return


    async def _get_html(self):
        """Retrieves html of the web page
        """
        self.html = await self.page.evaluate('document.documentElement.outerHTML')


    async def _response_processor(self, response):
        """Intercepts response and run processors
        """

        if response.status >=300:
            return

        await self._get_image_files(response)


    async def _get_image_files(self, response):
        """Intercepts image files downloads and store in self.image_files
        """

        url = response.url

        if '?' in url:
            url = url.split('?')[0]

        file_path = url.replace('/', '_')
        file_path = file_path.replace(':', '_')

        if len(file_path) > 40:
            file_path = file_path[-40:]

        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            a=1


        file_path = TEMP_DIR + '/' + file_path

        if response.request.resourceType == 'image':
            file = await response.buffer()
            image = {
                    '@type': 'schema:ImageObject',
                    'temp:data': file,
                    'schema:url': self.url,
                    'schema:contentUrl': response.url
                }
            self.images.append(image)

            # Below is for saving to file
            if 1 == 0:
                with open(file_path, "wb") as out:
                    out.write(file) 



        return

    def get_loop(self):
        return loop


async def pylaunch():

    """
    Launch chromium
    """


    global browser

    proxy_s = None
    
    while not proxy_s:
        proxy_s = FreeProxy(rand=True, country_id=['US', 'CA']).get()

    print('starting browser with proxy:', proxy_s)
    browser = await launch(
        options={
            'ignoreHTTPSErrors': True,
            'args': [
                    '--no-sandbox', '--proxy-server='+ proxy_s,
                    '--ignore-certificate-errors'
                    ]
            }, 
        headless = True, 
        defaultViewport = None,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
        )
    if browser:
        print('Browser started')
    return browser


loop = asyncio.get_event_loop()
browser = loop.run_until_complete(pylaunch())
print('browser started')
