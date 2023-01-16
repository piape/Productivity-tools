import sys
import subprocess

try:
    # 없는 모듈 import시 에러 발생
    import pandas as pd
except:
    # pip 모듈 업그레이드
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    
try:
    # 없는 모듈 import시 에러 발생
    import selenium
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'selenium'])

try:
    # 없는 모듈 import시 에러 발생
    import pyautogui
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pyautogui'])    
    
try:
    # 없는 모듈 import시 에러 발생
    import chromedriver_autoinstaller
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'chromedriver_autoinstaller'])

# 셀레니움 옵션
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 모듈 임포트
import os
import warnings
warnings.filterwarnings('ignore')
import time
import pandas as pd
import pyautogui
import chromedriver_autoinstaller


# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
chrome_options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
chrome_options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.
# chrome_options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
# chrome_options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
# chrome_options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
# chrome_options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.


# 1. 현재창에서 셀레니움을 실행 할지 설정
def openChromeSelenium(isopenChromeSelenium=False):
    if isopenChromeSelenium:
        # cmd 창을 실행해서 현재 크롬에서 실행
        pyautogui.hotkey("win", "r")  # 단축키 : win + r 입력
        pyautogui.write('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium_chrome"')  # 프로그램 명 입력
        pyautogui.press("enter")  # 엔터 키 입력

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


# 2. 크롬에서 파일 다운로드 경로 설정하기
def setDownLoadPath(download_path=None):
    # download_path = "down_load_path"
    if download_path != None:
        # os.path.abspath("Scripts") : 현재 작업 경로에 Scripts를 더함   =>  "C:\Python35\Scripts" 현재 경로에  download_path = os.path.abspath(download_path)
        prefs = {"download.default_directory": download_path}
        print(download_path)
        chrome_options.add_experimental_option("prefs", prefs)

# 3. 크롬 드라이버 자동으로 설치하게
def autoInstallerChromeDriver():
    global driver_path
    # 크롬을 자동으로 받게 하는 옵션 / 설치되어 있는지 확인
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrome driver is installed: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

# 자동으로 설치하기
autoInstallerChromeDriver()

# 수집 폴더 생성
try :
    os.mkdir('./collect_list')
except :
    pass

# 수집시간 표시기
now = time.strftime('%Y-%m-%d')
print(f'수집시간 : {now}')

# 자동검색 오프너
def search_open(keyword):
    print('국내 논문 수집을 시작합니다.\n')
    driver.find_element(By.ID,'query').send_keys(keyword)
    driver.find_element(By.XPATH,'//*[@id="in"]/div/button').click() # 검색 클릭
    
    print('해당 키워드 검색결과 \n - 학술지 논문 : 총', driver.find_element(By.CSS_SELECTOR,'div:nth-child(1) > div.title > h3 > span').text, '건\n\n')
    time.sleep(1)
    
    driver.find_element(By.XPATH,'//*[@id="divContent"]/div/div/div[2]/div[1]/div[2]/a/img').click()
    time.sleep(1)

    # 디스플레이 개수 사전설정
    max_show()
    
    for y in range(int(year_start), int(year_end)+1):
        # 수집 데이터 초기화
        datas = []
        
        # 상세 검색
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="TopSearch"]/fieldset/div/button').click() # 상세검색 클릭 search
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="RissDetailSearch"]/fieldset/div[1]/div[1]/ul/li[1]/label').click() # 국내학술논문 클릭
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="detailSrch1"]/div[1]/div/div[1]/label').click() # 필터설정
        time.sleep(0.5)
        driver.find_element(By.LINK_TEXT, '전체').click()
        time.sleep(1)
        
        # KCI 체크여부 확인 #
        driver.find_element(By.XPATH,'//*[@id="detailSearcjOption4"]/div/ul/li[1]/label/span').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="detailSearcjOption4"]/div/ul/li[2]/label/span').click()
        time.sleep(0.5)
        
        
        # 키워드, 연도 설정        
        keyword_years(keyword, y)
    
        # 수집할 논문 수 표시
        
        print(y,'년 검색결과 : ', 
              driver.find_element(By.CSS_SELECTOR, 'div.rightContent.wd756 > div > div.searchBox > dl > dd > span > span').text,'건')

        # 수집기 실행
        try:
            for j in range(3, 11) :  
                for i in range(1, 101):
                    label_from_web = []
                    title = []                    
                    year = []
                    abstract = []

                    try:
                        label_from_web = int(driver.find_element(By.CSS_SELECTOR,'li:nth-child('+str(i)+') > span.num.wd45 > label').text)        
                    except :
                        break                  
                    try:
                        year = int(driver.find_element(By.CSS_SELECTOR,'li:nth-child('+str(i)+') > div.cont.ml60 > p.etc > span:nth-child(3)').text)
                    except :
                        year = 'NaN'                  
                    try:
                        title = driver.find_element(By.CSS_SELECTOR,'li:nth-child('+str(i)+') > div.cont.ml60 > p.title > a').text
                    except :
                        title = 'NaN'              
                    try:
                        abstract = driver.find_element(By.CSS_SELECTOR,'li:nth-child('+str(i)+') > div.cont.ml60 > p.preAbstract').text
                    except :
                        abstract = 'NaN'

                    datas.append({'label_from_web' : label_from_web, 'title' : title, 'year' : year, 'abstract' : abstract})

                    
                if driver.find_element(By.CSS_SELECTOR,'div.paging > a:nth-child('+str(j)+')').text == '맨끝 페이지로':
                    break                   
                else:    
                    driver.find_element(By.CSS_SELECTOR,'div.paging > a:nth-child('+str(j)+')').click() # 페이지 넘기기
                    time.sleep(1)

                time.sleep(1)    
            print(f' - {y}년 수집 종료, {len(datas)}건\n')
            
        except:
            pass     
        
       
        #데이타프레임으로 변환
        df = pd.DataFrame(datas)
        
        # csv 저장
        df.to_csv(f'./collect_list/[{y}]_{keyword}.csv', index=False)

    print('프로그램 종료')

def keyword_years(keyword, y):
    driver.find_element(By.ID,'keyword1').send_keys(keyword) # 키워드 입력
    time.sleep(1)
    driver.find_element(By.ID,'p_year1').send_keys(y) # 시작연도
    driver.find_element(By.ID,'p_year2').send_keys(y) # 종료연도
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="RissDetailSearch"]/fieldset/div[2]/a[1]').click() # 실행
    time.sleep(1)

def max_show():
    # 디스플레이 개수 변환
    driver.find_element(By.XPATH,'//*[@id="divContent"]/div/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[1]/label').click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, '100개씩 출력').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="divContent"]/div/div[2]/div/div[3]/div[1]/div[2]/button').click() # 클릭
    time.sleep(1)

# 사용자입력
print("검색 키워드를 입력해주세요")
keyword = input() # keyword
print("시작년도를 입력해주세요(최소)")
year_start = input()
print("종료년도를 입력해주세요(최대)")
year_end = input()

# 웹 구동
driver = webdriver.Chrome(f'{driver_path}')
url = 'http://www.riss.kr/index.do'
driver.get(url)
time.sleep(1)


# 실행
search_open(keyword)


