### v2
import requests
import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import datetime
import calendar


def post_message(token, channel, text):
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + token},
                  data={"channel": channel, "text": text}
                  )


class DailyAttendance():
    def __init__(self, type=''):
        self.failed = False
        self.year = datetime.datetime.today().year
        self.month = datetime.datetime.today().month
        self.today = datetime.datetime.today().day
        self.last_day = calendar.monthrange(self.year, self.month)[1]
        self.channel_name = "#daily_attendance"
        self.slack_token = 'xoxb-'
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
        print("%s" % self.day)

    def login(self, com_cate):
        try:
            self.login_check = True
            url_dict = {
                "gmarket": "https://signinssl.gmarket.co.kr/login/login?url=http://promotion.gmarket.co.kr/Event/PlusZone.asp",
                "11": "https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fpromo.11st.co.kr%2Fview%2Fp%2F20210101-11check",
                "gs": "https://www.gsshop.com/cust/login/login.gs?returnurl=68747470733A2F2F6576656e742e677373686f702e636f6d2F6576656e742F70632F617474656e642e67733F",
                "sidmool": "https://www.sidmool.com/shop/member.html?type=login",
            }
            cookie_dict = {"gmarket": "shipnation",
                           "11": "TMALL_AUTH",
                           "gs": "username",
                           "sidmool": "user_age", }
            self.driver.get(url_dict[com_cate])
            try:
                if 'gmarket' in com_cate:
                    self.driver.find_element_by_name('id').send_keys(self.data[0])
                    self.driver.find_element_by_name('pwd').send_keys(self.data[1], Keys.ENTER)
                elif '11' in com_cate:
                    self.driver.find_element_by_name('loginName').send_keys(self.data[0])
                    self.driver.find_element_by_name('passWord').send_keys(self.data[2], Keys.ENTER)
                elif 'sidmool' in com_cate:
                    self.driver.find_element_by_name('id').send_keys(self.data[0])
                    self.driver.find_element_by_name('passwd').send_keys(self.data[2], Keys.ENTER)
                elif 'gs' in com_cate:
                    self.driver.find_element_by_id('id').click()
                    self.driver.find_element_by_id('id').send_keys(self.data[0])
                    self.driver.find_element_by_name('passwd').send_keys(self.data[2], Keys.ENTER)
                ## cookie 로딩을 위한 시간
                time.sleep(1)
                if self.driver.get_cookie(cookie_dict[com_cate]) is not None:
                    self.login_check = False
            except Exception as e:
                post_message(self.slack_token, self.channel_name, "%s login failed\n %s" % (com_cate, e))
            if not self.login_check:
                print("%s started" % com_cate)
                time.sleep(2)
            else:
                print("%s couldn't login" % com_cate)
                post_message(self.slack_token, self.channel_name, "%s couldn't login" % com_cate)
        except Exception as e:
            self.login_check = True
            print("%s exception" % com_cate)
            post_message(self.slack_token, self.channel_name, "%s exception\n %s" % (com_cate, e))
            pass

    def attend(self, com_cate):
        try:
            if 'gmarket' in com_cate:
                self.driver.switch_to.frame('AttendRulletFrame')  # 룰렛 프레임으로 진입
                attend = self.driver.find_element_by_css_selector('#wrapper > a').get_attribute('onclick')
                self.driver.execute_script(attend)
                time.sleep(5)  # 룰렛 돌아가는 시간
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
                self.driver.switch_to.parent_frame()  # 메인 프레임으로 돌아가기
                # 10,15,마지막일 포인트 받기
                if self.today == self.last_day:
                    gm_cssselector_list = [
                        '#event_pluszone > div.event_main > div > div.area.attendance > div.attendance_benefit > ul > li:nth-child(1) > a > img',
                        '#event_pluszone > div.event_main > div > div.area.attendance > div.attendance_benefit > ul > li:nth-child(2) > a > img',
                        '#event_pluszone > div.event_main > div > div.area.attendance > div.attendance_benefit > ul > li:nth-child(3) > a > img']
                    for cssselector in gm_cssselector_list:
                        self.driver.find_element_by_css_selector(cssselector).click()
                        time.sleep(2)  # 팝업 대기하는 시간
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
            elif '11' in com_cate:
                self.driver.execute_script('onAttendanceClick();')  # 메인 출첵
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass
                if self.today == self.last_day:
                    ## 5,15,마지막일 포인트 받기
                    st11_cssselector_list = ['#fiveAttendanceBtn > a', '#fifteenAttendanceBtn > a', '#allAttendanceBtn > a']
                    for cssselector in st11_cssselector_list:
                        st11_script = self.driver.find_element_by_css_selector(cssselector).get_attribute('onclick')
                        st11_script = str(st11_script).split(';')
                        self.driver.execute_script(st11_script[0])
                        time.sleep(1)
                        try:
                            result = self.driver.switch_to.alert
                            result.accept()
                        except:
                            pass
            elif 'sidmool' in com_cate:
                ## alert 두번 뜨는 경우 있음
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
            elif 'gs' in com_cate:
                # 메인 출첵
                self.gsattend = self.driver.find_element_by_css_selector(
                    '#attendchk > div.event-common-wrap > div.section2 > '
                    'div.attendchk-button > a').get_attribute('onclick')
                self.driver.execute_script(self.gsattend)
                time.sleep(3)
                self.driver.find_element_by_css_selector('#attendchk-popLayer > dl > dd > a').click()
                try:
                    result = self.driver.switch_to.alert
                    result.accept()
                except:
                    pass
                # 마지막 날 포인트 얻기
                try:
                    self.driver.find_element_by_css_selector(
                        '#attendchk > div.event-common-wrap > div.attend_take_point.disabled')
                    pass
                except:
                    if self.today == self.last_day:
                        self.driver.find_element_by_css_selector(
                            '#attendchk > div.event-common-wrap > div.attend_take_point > a').click()
            print("%s done" % com_cate)
        except Exception as e:
            print("%s couldn't attendance" % com_cate)
            post_message(self.slack_token, self.channel_name, "%s couldn't attendance\n %s" % (com_cate, e))
            self.failed = True

    def close(self):
        self.driver.quit()


def main():
    attend = DailyAttendance('hide')
    urllist = ['gmarket', '11', 'gs', 'sidmool']
    for url in urllist:
        attend.login(url)
        if not attend.login_check:
            attend.attend(url)
            pass
        else:
            pass
    attend.close()


main()
schedule.every().day.at("00:10").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
