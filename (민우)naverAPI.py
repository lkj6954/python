import os
import sys
import urllib.request
import json
import time
import pandas as pd

client_id = "rljYOVvvo9n6oI6WRU2d"
client_secret = "LkoGP2WjTk"

url = "https://openapi.naver.com/v1/datalab/search"

startDate = input('조회 시작 날짜 입력(예시:2000-01-01):')
endDate = input('조회 종료 날짜 입력(예시:2000-01-01):')

groupName = input('그룹 네임1:')
keyword = input('키워드1:')

soondae = input('그룹 네임2:')
s_keyword = input('키워드2:')

## https://developers.naver.com/docs/datalab/search/  네이버 api json 형식

body = {
    'startDate' : startDate,
    'endDate' : endDate,
    'timeUnit' : 'date',        # input : [date, week, month]
    'keywordGroups' : [         
        {
            'groupName': groupName,
            'keywords': [keyword]
        },
        {
            'groupName':soondae,
            'keywords' : [s_keyword]
        }
    ],
}
body = json.dumps(body)

request = urllib.request.Request(url)

request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))

rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

data = json.loads(response_body.decode('utf-8'))

d_df = pd.DataFrame(data['results'][0]['data'])
d_df.columns=['기간','돼지국밥']
d_df.set_index('기간')

s_df = pd.DataFrame(data['results'][1]['data'])
s_df.columns=['기간','순대국']
s_df.set_index('기간')

df = d_df.merge(s_df, how='outer', on='기간').fillna(0)

print(df)

f_dir = "C:\\Users\\dlals\\Desktop\\project_code\\"

# 저장될 파일위치와 이름을 지정합니다
n = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (n.tm_year, n.tm_mon, n.tm_mday, n.tm_hour, n.tm_min, n.tm_sec)

os.makedirs(f_dir+s+'-'+'데이터랩')
os.chdir(f_dir+s+'-'+'데이터랩')

fc_name=f_dir+s+'-'+'데이터랩'+'\\'+s+'-'+'데이터랩'+'.csv'

df.to_csv(fc_name,encoding="utf-8-sig",index=False)