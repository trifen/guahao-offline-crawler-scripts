#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import requests
import traceback

# Global Variables

wait = 1
defaultSeperator = ','
defaultHeaders = {'User-Agent':'','Cookie':'_sid_=1'}
resultHeaders = [ '医生姓名','医生ID','患者ID',
                  '满意度','疾病','治疗方式','病情状况',
                  '评论内容','评论时间','评论来源' ]

sourceFilePath = './step-1-result.csv'
resultFilePath = './step-2-2-result.csv'

# GRAB DOCTOR INFO

print('Starting crawling comments ...')

counter = 0

with open(sourceFilePath) as sf:

    # skip header line
    next(sf)

    with open(resultFilePath, 'w') as rf:

        rf.write(defaultSeperator.join(resultHeaders))

        for row in sf:

            [drName,drID,hosN,depN] = row.strip().split(defaultSeperator)
            counter+=1
            print('No '+str(counter)+', Crawling comments of '+drName+', '+drID)

            stop   = False
            pageNo = 0
            extra  = ''

            while not stop:

                # next page
                pageNo += 1
                print('Crawling comments page '+str(pageNo))

                baseUrl = 'https://www.guahao.com/commentslist/e-'+str(drID)+'/all-0'

                if pageNo == 1:
                    sourceUrl = baseUrl
                else:
                    sourceUrl = baseUrl+'?pageNo='+str(pageNo)+extra

                try:
                    # CRAWL COMMENTS
                    res = requests.get(sourceUrl, headers=defaultHeaders)
                    soup = BeautifulSoup(res.text,'html.parser')

                    inputs = soup.select('div.g-pagination-buttom input > input')
                    if len(inputs) > 0:
                        extra = '&sign='+inputs[0].get('value')+'&timestamp='+inputs[1].get('value')

                    commentsList = soup.select('#comment-list > li')

                    # stop on empty list
                    if len(commentsList) == 0:
                        stop = True
                        break

                    for cm in commentsList:

                        userName = cm.select('div.user p')[0].text.strip()

                        row1 = cm.select('div.row-1')[0]

                        attitude = ''
                        pa = row1.select('p.attitude > strong')
                        if len(pa) > 0:
                            attitude = pa[0].text.strip()

                        disease  = ''
                        treat    = ''
                        status   = ''
                        pd = row1.select('span')
                        if len(pd) > 0:
                            disease = pd[0].text.strip()
                        if len(pd) > 2:
                            treat   = pd[1].text.strip()
                            status  = pd[2].text.strip()

                        row2 = cm.select('div.row-2')[0]
                        cText = ''
                        cTimeSrc = ','
                        pt = row2.select('div.text > span')
                        if len(pt) > 0:
                            cText = pt[0].text.strip()
                            cTimeSrc = defaultSeperator.join([' '.join(s.text.strip().split()) for s in row2.select('div.info > p > span')])

                        rf.write('\n'+defaultSeperator.join([drName,drID,userName,attitude,
                                                             disease,treat,status,
                                                             cText,cTimeSrc]))
                except Exception as e:
                    traceback.print_exc()
                    exit(1)

print('Finished crawling comments.\n')
