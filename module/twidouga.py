import requests
from bs4 import BeautifulSoup
import lxml
import ssl
from module.module import Modules
from schema.db import DB

class Twidouga():

    def __init__(self) -> None:
        ssl._create_default_https_context = ssl._create_unverified_context

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
        urls = ["https://www.twidouga.net/ranking_t.php", "https://www.twidouga.net/ranking_t2.php"]
        header = {
                "User-Agent": user_agent,
        }
        
        self.converted_html: list[BeautifulSoup] = []

        for url in urls:
            self.converted_html.append(
                self.__createbs(url, header)
            )

    def __createbs(self, url: str, header: dict) -> BeautifulSoup:
        try:
            response = requests.get(url, headers = header)
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        except Exception as e:
            print(e)
            print("エラー")
            return None

    def __get_all_video_link(self, bs: BeautifulSoup) -> list[str]:
        divs = bs.find_all("div", attrs={"class": "poster"})
        a_tag = [d.find("a") for d in divs]
        hrefs = [a.get('href') for a in a_tag]
        return hrefs

    def do(self):
        db = DB()
        for target in self.converted_html:
            for video in self.__get_all_video_link(target):
                id = Modules.extract_file_name_from_url(video)
                if db.check_url_exists(id):
                    print("スキップします：{}".format(id))
                    continue
                print("ダウンロードします：{}".format(id))
                Modules.download_mp4(video)
                db.insert_single_url(Modules.extract_file_name_from_url(video))

    def test(self):
        print("test")


