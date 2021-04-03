import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle


class DailyAttendance():
    def __init__(self, type):
        if 'hide' in type:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 "
                "Safari/537.36")
            self.driver = webdriver.Chrome('./chromedriver', options=options)
        else:
            self.driver = webdriver.Chrome('./chromedriver')
            self.driver.implicitly_wait(3)
        self.day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with open('data.plk', 'rb') as f:
            self.data = pickle.load(f)
        self.login_check = True
        self.count = 1
        print("%s" % self.day)

    def login(self, com):
        try:
            if 'gmarket' in com:
                self.driver.get('https://signinssl.gmarket.co.kr/login/login?url='
                                'http://promotion.gmarket.co.kr/Event/PlusZone.asp')
                self.driver.find_element_by_name('id').send_keys(self.data[0])
                self.driver.find_element_by_name('pwd').send_keys(self.data[1], Keys.ENTER)
                self.driver.switch_to.frame('AttendRulletFrame')
            elif '11' in com:
                self.driver.get(
                    'https://login.11st.co.kr/auth/front/login.tmall?returnURL='
                    'https%3A%2F%2Fpromo.11st.co.kr%2Fview%2Fp%2F20210101-11check')
                self.driver.find_element_by_name('loginName').send_keys(self.data[0])
                self.driver.find_element_by_name('passWord').send_keys(self.data[2], Keys.ENTER)
                self.driver.execute_script('onAttendanceClick();')
            elif 'sidmool' in com:
                self.driver.get('https://www.sidmool.com/shop/member.html?type=login')
                self.driver.find_element_by_name('id').send_keys(self.data[0])
                self.driver.find_element_by_name('passwd').send_keys(self.data[2], Keys.ENTER)
                ### login check
                self.driver.get_cookie('user_age')
            elif 'gs' in com:
                self.driver.get('https://www.gsshop.com/cust/login/login.gs?'
                                'returnurl=68747470733A2F2F6576656e742e677373686f702e636f6d2F6576656e742F70632F617474656e642e67733F')
                self.driver.find_element_by_id('id').click()
                self.driver.find_element_by_id('id').send_keys(self.data[0])
                self.driver.find_element_by_name('passwd').send_keys(self.data[2], Keys.ENTER)
                time.sleep(2)
                self.gsattend = self.driver.find_element_by_css_selector(
                    '#attendchk > div.event-common-wrap > div.section2 > '
                    'div.attendchk-button > a').get_attribute('onclick')
            print("%s started" % com)
            self.login_check = False
        except Exception as e:
            print(e)
            print("%s couldn't login" % com)
            self.login_check = True
            while self.login_check:
                print("%s trying" % com)
                time.sleep(360)
                self.login(com)

    def attend(self, com):
        if 'gmarket' in com:
            attend = self.driver.find_element_by_css_selector('#wrapper > a').get_attribute('onclick')
            self.driver.execute_script(attend)
            time.sleep(10)
            if len(self.driver.window_handles) == 2:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass

            self.driver.switch_to.parent_frame()
            self.driver.find_element_by_css_selector(
                '#event_pluszone > div.event_main > div > div.area.attendance > '
                'div.attendance_benefit > ul > li:nth-child(1) > a > img').click()
            time.sleep(2)
            if len(self.driver.window_handles) == 2:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.find_element_by_css_selector('body > div.popTypeB > div > '
                                                         'div.btnWrap > a > img').click()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass

            self.driver.find_element_by_css_selector(
                '#event_pluszone > div.event_main > div > div.area.attendance > '
                'div.attendance_benefit > ul > li:nth-child(2) > a > img').click()
            time.sleep(2)
            if len(self.driver.window_handles) == 2:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.find_element_by_css_selector('body > div.popTypeB > div > '
                                                         'div.btnWrap > a > img').click()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass

            self.driver.find_element_by_css_selector(
                '#event_pluszone > div.event_main > div > div.area.attendance > '
                'div.attendance_benefit > ul > li:nth-child(3) > a > img').click()
            time.sleep(2)
            if len(self.driver.window_handles) == 2:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.find_element_by_css_selector('body > div.popTypeB > div > '
                                                         'div.btnWrap > a > img').click()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass
        elif '11' in com:
            time.sleep(1)
            try:
                result = self.driver.switch_to.alert
                result.accept()
            except:
                pass
            get5day = self.driver.find_element_by_css_selector('#fiveAttendanceBtn > a').get_attribute('onclick')
            get5day = str(get5day).split(';')
            self.driver.execute_script(get5day[0])
            time.sleep(1)
            try:
                result = self.driver.switch_to.alert
                result.accept()
            except:
                pass
            get15day = self.driver.find_element_by_css_selector('#fifteenAttendanceBtn > a').get_attribute(
                'onclick')
            get15day = str(get15day).split(';')
            self.driver.execute_script(get15day[0])
            time.sleep(1)
            try:
                result = self.driver.switch_to.alert
                result.accept()
            except:
                pass
            getall = self.driver.find_element_by_css_selector('#allAttendanceBtn > a').get_attribute('onclick')
            getall = str(getall).split(';')
            self.driver.execute_script(getall[0])
            time.sleep(1)
            try:
                result = self.driver.switch_to.alert
                result.accept()
            except:
                pass
        elif 'sidmool' in com:
            time.sleep(2)
            try:
                result = self.driver.switch_to.alert
                result.accept()
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass
            except:
                pass
        elif 'gs' in com:
            self.driver.execute_script(self.gsattend)
            time.sleep(1)
            self.driver.find_element_by_css_selector('#attendchk-popLayer > dl > dd > a').click()
            try:
                result = self.driver.switch_to.alert
                result.accept()
                self.driver.find_element_by_css_selector(
                    '#attendchk > div.event-common-wrap > div.attend_take_point > a').click()
            except:
                pass
        print("%s done" % com)
        time.sleep(2)

    def close(self):
        self.driver.quit()


def main():
    attend = DailyAttendance('hide')
    urllist = ['gmarket', '11', 'gs', 'sidmool']
    for url in urllist:
        attend.login(url)
        if not attend.login_check:
            attend.attend(url)
        else:
            pass
    attend.close()


main()
schedule.every().day.at("00:10").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
