from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import ast
import ddddocr


class AutoLogin:
    def __init__(self, url, path, name='', pswd=''):
        self.driver = webdriver.Chrome()
        self.name = name
        self.url = url
        self.pswd = pswd

    def get_image_code(self, image_bytes):
        ocr = ddddocr.DdddOcr()

        text = ocr.classification(image_bytes)

        return text
    def get_params(self):
        # 获得必要参数
        while 1:
            self.driver.get(self.url)
            time.sleep(2)
            self.driver.implicitly_wait(15)
            name_ele = self.driver.find_element(By.XPATH,'//input[@id="loginName"]')
            name_ele.send_keys(self.name)
            pswd_ele = self.driver.find_element(By.XPATH,'//input[@id="loginPwd"]')
            pswd_ele.send_keys(self.pswd)

            el_image_code = self.driver.find_element(By.ID, "vcodeImg")#验证码图片
            text_code = self.get_image_code(el_image_code.screenshot_as_png)

            el_input = self.driver.find_element(By.XPATH,'//input[@id="verifyCode"]')#验证码输入框
            el_input.send_keys(text_code)

            start_ele = self.driver.find_element(By.XPATH, '//button[@id="studentLoginBtn"]')#开始按钮
            start_ele.click()


            time.sleep(1)
            sure_ele = self.driver.find_element(By.XPATH, '//*[@id="errorMsg"]')
            if not sure_ele.is_displayed():
                sure1_ele = self.driver.find_element(By.XPATH, '//*[@id="buttons"]/button[2]')
                sure1_ele.click()
                sure2_ele = self.driver.find_element(By.XPATH, '//button[@id="courseBtn"]')
                sure2_ele.click()
                break



        if WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'aPublicCourse'))):
            time.sleep(1)  # waiting for loading
            cookie_lis = self.driver.get_cookies()
            cookies = ''
            for item in cookie_lis:
                cookies += item['name'] + '=' + item['value'] + '; '
            token = self.driver.execute_script('return sessionStorage.getItem("token");')
            batch_str = self.driver. \
                execute_script('return sessionStorage.getItem("currentBatch");').replace('null', 'None').replace('false', 'False').replace('true', 'True')
            batch = ast.literal_eval(batch_str)
            self.driver.quit()

            return cookies, token, batch['code']

        else:
            print('page load failed')
            self.driver.quit()
            return False

    # 暂时无用
    def keep_connect(self):
        flag = 1
        st = time.perf_counter()
        while True:
            try:
                if flag == 1:
                    ele = self.driver.find_element_by_xpath('//a[@id="aPublicCourse"]')
                    ele.click()
                    flag = 2
                    time.sleep(30)
                elif flag == 2:
                    ele = self.driver.find_element_by_xpath('//a[@id="aProgramCourse"]')
                    ele.click()
                    flag = 1
                    time.sleep(30)

            except NoSuchElementException:
                print('连接已断开')
                print(f'运行时间：{(time.perf_counter() - st)//60} min')
                # self.driver.quit()
                break


if __name__ == '__main__':
    Url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'
    Name = ''
    Pswd = ''
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36'
    }
