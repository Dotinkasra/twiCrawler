from module.twidouga import Twidouga
from module.twivideo import Twivideo
import schedule
from time import sleep
class Main():
    def __init__(self) -> None:
        self.twidouga = Twidouga()
        self.twivideo = Twivideo()
        schedule.every().days.at("12:00").do(self.twidouga.do)
        schedule.every().days.at("12:00").do(self.twivideo.do)

    def main(self):
        while True:
            schedule.run_pending()
            sleep(1)


main = Main()
main.main()