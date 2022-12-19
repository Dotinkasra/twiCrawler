import requests
from bs4 import BeautifulSoup
import lxml
import ssl
from module.module import Modules
from schema.db import DB
from selenium import webdriver
import time
class Twivideo():

    def __init__(self) -> None:
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
        urls = ["https://twivideo.net/?ranking"]
        header = {
                "User-Agent": user_agent,
        }
        driver_path = "/Users/twemu/bin/chromedriver"
        browser_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        options = webdriver.ChromeOptions()
        options.binary_location = browser_path
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=driver_path, options = options)
        driver.get(urls[0])
        time.sleep(3)
        self.converted_html = self.__createbs(driver.page_source.encode('utf-8'))

    def __createbs(self, html) -> BeautifulSoup:
        try:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as e:
            print(e)
            print("エラー")
            return None

    def __get_all_video_link(self, bs: BeautifulSoup) -> list[str]:
        div = bs.find("div", attrs={"class": "grids"})
        a_link = div.find_all("a", attrs={"class": "item_clk item_link"})
        hrefs = [a.get('href') for a in a_link]
        return hrefs

    def do(self):
        db = DB()  
        for video in self.__get_all_video_link(self.converted_html):
            id = Modules.extract_file_name_from_url(video)
            if db.check_url_exists(id):
                print("スキップします：{}".format(id))
                continue
            print("ダウンロードします：{}".format(id))
            Modules.download_mp4(video)
            db.insert_single_url(Modules.extract_file_name_from_url(video))

    def test(self):
        print("test")


