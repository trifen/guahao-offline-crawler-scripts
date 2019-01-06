#-*-coding:UTF-8-*-
#-*-encoding=UTF-8-*-

from bs4 import BeautifulSoup
from time import sleep
import requests
import traceback

# Global Variables

wait = 1

# guahao地区代码
guahaoAreaCode = {
    2: '上海'
}

# guahao科室ID:
guahaoDepartmentID = {
    '7f67dd62-cff3-11e1-831f-5cf9dd2e7135':'骨科',
    '7f6802e2-cff3-11e1-831f-5cf9dd2e7135':'儿科',
    '7f682eb6-cff3-11e1-831f-5cf9dd2e7135':'儿童骨科'
}

# defaultHeaders = {'User-Agent': ''}
defaultSeperator = ','
resultHeaders = [ '医生姓名','医生ID' ]
resultFilePath = './step-1-result.csv'

# GRAB DOCTOR LINKS
# https://www.guahao.com/search/expert?iSq=1&standardDepartmentId=7f67dd62-cff3-11e1-831f-5cf9dd2e71352&pageNo=1

print('Starting crawling doctor links ...')

doctorIDDict = dict()

with open(resultFilePath, "w") as rf:

    rf.write(defaultSeperator.join(resultHeaders))

    counter = 0

    for code,area in guahaoAreaCode.items():

        print('Crawling ' + area + ' doctor links ...')

        for dpID,dpName in guahaoDepartmentID.items():

            stop   = False
            pageNo = 0

            while not stop:

                # next page
                pageNo += 1
                print('Crawling '+dpName+' doctor link, page '+str(pageNo))

                sourceUrl = 'https://www.guahao.com/search/expert?iSq=1&&pi='+str(code)+'&standardDepartmentId='+str(dpID)+'&pageNo='+str(pageNo)

                try:

                    res = requests.get(sourceUrl)
                    soup = BeautifulSoup(res.text,'html.parser')
                    doctorList = soup.select('[class*=g-doctor-item]')

                    # stop on empty list
                    if len(doctorList) == 0:
                        stop = True
                        break

                    for dt in doctorList:
                        doctor = dt.select('dt')[0].select('a')[0]
                        key = defaultSeperator.join([doctor['title'], doctor['monitor-doctor-id']])
                        if not key in doctorIDDict:
                            doctorIDDict[key] = True
                            rf.write('\n'+key)
                            counter+=1

                except Exception as e:
                    traceback.print_exc()
                    exit(1)

                sleep(float(wait))

print('Finished crawling doctor links, totally '+str(counter)+' doctors collected.\n')
