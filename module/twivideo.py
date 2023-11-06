from bs4 import BeautifulSoup
from module.module import Modules
from schema.db import DB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
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

    def do(self):
        print("実行します:{}".format(datetime.datetime.now()))

        ret_links_from_webd = []
        for url in self.urls:
            webd = self.TwivideoDlWithWebDriver(url)
            ret_links_from_webd.append(webd.get_all_video_link())

        video_links = [
            video_link 
            for ret_link in ret_links_from_webd
            for video_link in ret_link 
        ]

        db: DB = DB()
        for url in video_links:
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

    class TwivideoDlWithWebDriver():
        def __init__(self, url: str) -> None:
            driver_path = "/Users/twaoi/bin/chromedriver"
            browser_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

            options = webdriver.ChromeOptions()
            options.binary_location = browser_path

            download_path = "/Users/twaoi/Server/schedule_app/movie"
            options.add_experimental_option("prefs", {"download.default_directory": download_path})

            self.driver = webdriver.Chrome(executable_path=driver_path, options = options)
            self.driver.get(url)

            time.sleep(10)

        def get_all_video_link(self) -> list[str]:
            grids = self.driver.find_elements(By.CSS_SELECTOR, "div.grids a.item_clk.item_link")
            urls = []
            for i in grids:
                print("実行")
                try:
                    i.click()
                    time.sleep(5)
                    
                    if len(self.driver.window_handles) > 1:
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        urls.append(self.driver.current_url)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                except Exception as e:
                    print(e)
                finally:
                    continue
            self.driver.close()
            return urls
    




