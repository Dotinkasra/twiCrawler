from bs4 import BeautifulSoup
from module.module import Modules
from schema.db import DB
from selenium import webdriver
import time
import datetime

class Twivideo():
    def __init__(self) -> None:
        print("twivideo")
        self.urls = [
            "https://twivideo.net/?ranking",
            "https://twivideo.net/?ranking&sort=3days",
            "https://twivideo.net/?ranking&sort=week"
        ]

    def __get_dynamic_site_html(self, url):
        driver_path = "/Users/twemu/bin/chromedriver"
        browser_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

        options = webdriver.ChromeOptions()
        options.binary_location = browser_path
        options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path=driver_path, options = options)
        driver.get(url)
        time.sleep(3)

        return driver.page_source.encode('utf-8')

    def __createbs(self, html) -> BeautifulSoup:
        try:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as e:
            print(e)
            print("エラー")
            return None

    def __get_all_video_link(self, bs: BeautifulSoup) -> list[str]:
        try:
            div = bs.find("div", attrs={"class": "grids"})
            a_link = div.find_all("a", attrs={"class": "item_clk item_link"})
            hrefs = [a.get('href') for a in a_link]
            return hrefs
        except Exception as e:
            print(e)
            return []     
        
    def __get_download_video_link(self) -> list[str]:
        db: DB = DB()
        urls: list[str] = []
        for url in self.urls:
            converted_html: BeautifulSoup = self.__createbs(self.__get_dynamic_site_html(url))
            if not converted_html: continue
            for video in self.__get_all_video_link(converted_html):
                if db.check_url_exists(video):
                    print("Twivideo : スキップします：{}".format(video))
                    continue
                urls.append(video)
        del db
        return urls

    def do(self):
        print("実行します:{}".format(datetime.datetime.now()))

        db: DB = DB()
        for url in self.__get_download_video_link():
            try:
                Modules.download_mp4(url)
                db.insert_single_url(url)
                print("Twivideo : ダウンロードします：{}".format(url))
            except Exception as e:
                print(e)
            finally:
                continue

    def test(self):
        self.do()


