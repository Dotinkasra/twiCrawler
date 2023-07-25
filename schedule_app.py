from module.twidouga import Twidouga
from module.twivideo import Twivideo
import schedule
from time import sleep
class Main():
    def __init__(self) -> None:
        self.twidouga = Twidouga()
        self.twivideo = Twivideo()
        #schedule.every().days.at("12:25").do(self.twidouga.do)
        #schedule.every().days.at("12:25").do(self.twivideo.do)
        schedule.every(2).hours.do(self.twivideo.do)
        schedule.every(2).hours.do(self.twidouga.do)

    def main(self):
        print("起動")
        self.twidouga.do()
        self.twivideo.do()
        while True:
            schedule.run_pending()
            sleep(1)

    def test(self):
        self.twidouga.test()
        self.twivideo.test()

main = Main()
main.main()