import re
import requests
import os

class Modules():

    @classmethod
    def extract_file_name_from_url(self, url: str) -> str | None:
        # 正規表現を使用して、URLの末尾にある文字列を取得
        match = re.search(r'[^/]+\.mp4', url)
        if match:
            # マッチした文字列を返す
            return match.group()
        else:
            return None

    @classmethod
    def download_mp4(self, url: str, count: int = 0):
        if count > 5 or str is None or str == "":
            return
        try:
            response = requests.get(url)
        except Exception as e:
            print(url, e)
            return
        
        id = self.extract_file_name_from_url(url)
        if id is None or id == '':
            return
        file_name = "./movie/" + id
        try:
            with open(file_name, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)

        if os.stat(file_name).st_size == 0:
            os.remove(file_name)
            return self.download_mp4(file_name, count = count + 1)
