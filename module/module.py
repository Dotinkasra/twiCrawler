import re
import requests
from schema.db import DB
class Modules():

    @classmethod
    def extract_file_name_from_url(self, url: str) -> str:
        # 正規表現を使用して、URLの末尾にある文字列を取得
        match = re.search(r'[^/]+(?=\?)', url)
        if match:
            # マッチした文字列を返す
            return match.group()
        else:
            return None

    @classmethod
    def download_mp4(self, url: str):
        response = requests.get(url)
        id = self.extract_file_name_from_url(url)
        if id is None or id == '':
            return
        file_name = "./movie/" + id
        try:
            open(file_name, 'wb').write(response.content)
        except Exception as e:
            print(e)