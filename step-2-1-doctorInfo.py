#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import requests
import traceback

# Global Variables

wait = 1
defaultSeperator = ','
resultHeaders = [ '医生姓名','医生ID','医院科室','医生职称',
                  '预约量','问诊量','综合评分',
                  '图文问诊价格','视话问诊价格','总评论人数' ]

sourceFilePath = './step-1-result.csv'
resultFilePath = './step-2-1-result.csv'

# GRAB DOCTOR INFO
# https://www.guahao.com/expert/f7ec9a00-e498-4f80-869c-8c2985864a40000

print('Starting crawling doctor info ...')

counter = 0

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(resultHeaders))

        for row in sf:

            [drName,drID] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling info of '+drName+', '+drID)

            try:
                # CRAWL DOCTOR LINKS
                sourceUrl = 'https://www.guahao.com/expert/'+str(drID)
                res = requests.get(sourceUrl)
                soup = BeautifulSoup(res.text,'html.parser')
                
                # Departments
                dps = []
                for p in soup.select('#card-hospital > p'):
                    dps.append('-'.join([a.text.strip() for a in p.select('a')]))
                departments = '|'.join(dps)

                # Occupation
                occ = ''.join([s.text.strip() for s in soup.select('div.detail.word-break > h1 > span')])

                # Data
                data = soup.select('div.data > div.total.fix-clear > strong')
                nApm = data[0].text
                nAcc = data[1].text
                eRate = soup.select('#expert-rate > a > strong')[0].text

                # Prices
                consulTypes = [l.select('p.current-price') for l in soup.select('div.consult-type > ul > li')]
                tuweiPrice  = ''.join([p.text for p in consulTypes[0]])
                shihuaPrice = ''.join([p.text for p in consulTypes[1]])

                # Comment
                nComment = soup.select('div.grid-title > div.tip > a > strong')[0].text

                rf.write('\n'+defaultSeperator.join([drName,drID,departments,occ,
                                                     nApm,nAcc,eRate,
                                                     tuweiPrice,shihuaPrice,nComment]))
            except Exception as e:
                traceback.print_exc()
                exit(1)

            sleep(float(wait))

print('Finished crawling doctor info.\n')
