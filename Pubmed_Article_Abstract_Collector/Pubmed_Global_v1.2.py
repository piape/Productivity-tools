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
    from Bio import Entrez, Medline
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'biopython==1.79'])


try:
    # 없는 모듈 import시 에러 발생
    from tqdm import tqdm
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'tqdm'])

import warnings
warnings.filterwarnings('ignore')
from io import StringIO
from Bio import Entrez, Medline
from tqdm import tqdm
import time
import os
import pandas as pd

# 수집시간 표시기
now = time.strftime('%Y-%m-%d')
print(f'수집시점 : {now}')

# 수집 폴더 생성
try :
    os.mkdir('./collect_list')
except :
    pass

def search_medline(query, email, year):
    Entrez.email = email
    search = Entrez.esearch(db='pubmed', term = query, usehistory='y', mindate = year, maxdate = year, retmax = 100000)
    handle = Entrez.read(search)
    try:
        return handle

    except Exception as e:
        print('error')
        raise IOError(str(e))

    finally:
        search.close()


def fetch_rec(rec_id, entrez_handle):
    fetch_handle = Entrez.efetch(db = 'pubmed', id = rec_id,
                                 rettype = 'Medline', retmode = 'text',
                                 webenv = entrez_handle['WebEnv'],
                                 query_key = entrez_handle['QueryKey'])
    rec = fetch_handle.read()
    return rec        


def main(query, email):
    print('--- --- --- '*5,'\n')
    print('# 논문 수집을 시작합니다.')
    print('# 수집 연도는', to_year,' ~ ', from_year,'입니다.\n')
    years = range(from_year, to_year -1, -1)
    
    for year in years:
        rec_handler = search_medline(query, email, year)
        print('--- --- --- '*5, '\n')
        print('#', year,'년의 논문은', len(rec_handler['IdList']),'건 입니다.\n')
        print('--- --- --- '*5, '\n')
        datas = []

        for rec_id in tqdm(rec_handler['IdList'], desc='수집률'):
            time.sleep(0.1)
            title = []
            p_date = []
            j_name = []
            p_country = []
            p_lang = []
            abst = []
            rec = fetch_rec(rec_id, rec_handler)
            rec_file = StringIO(rec)
            medline_rec = Medline.read(rec_file)
            time.sleep(0.1)
            if 'AB' in medline_rec:
                title = medline_rec['TI']
                p_date = medline_rec['DP']
                j_name = medline_rec['TA']
                p_country = medline_rec['PL']
                # p_lang = medline_rec['LA']
                abst = medline_rec['AB']
                # print('제목 : ', medline_rec['TI']) 
                # print('년도 : ', medline_rec['DP'])\
                # print('저널명 : ', medline_rec['TA'])
                # print('발행국가 : ', medline_rec['PL'])
                # print('언어 : ', medline_rec['LA'], '\n')
                # print('초록 : \n', medline_rec['AB'],'\n\n')          
            else :
                continue

            datas.append({'title' : title, 'p_date' : p_date, 'j_name' : j_name, 'p_country' : p_country,
                         'p_lang' : p_lang, 'abst' : abst})
                         
        df = pd.DataFrame(datas)
        df.to_csv(f'./collect_list/[{year}]_{query}.csv', index = False)
        
    print('프로그램 종료')      

if __name__ == '__main__':
    email = "abc@def.org"
    print('키워드를 입력하세요.')
    query = input()
    print('시작 년도를 입력하세요., ex> 2010')
    to_year = eval(input())
    print('종료 년도를 입력하세요., ex> 2022')
    from_year = eval(input())
    main(query, email)