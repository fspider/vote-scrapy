import scrapy
import pandas as pd
import bs4
from bs4 import *
import os
from scrapy.crawler import CrawlerProcess
import csv

class QuotesSpider(scrapy.Spider):
    name = "BoothSpider"
    ctr=0
    def __init__(self):
        self.individualSavePath = "individual.csv"
        self.familySavePath = "family.csv"

        self.individualFile = None
        self.familyFile = None
        # self.individualFile = open(self.individualSavePath, "w", encoding="utf-8", newline="")
        # self.individualWriter = csv.writer(self.individualFile)

        # self.familyFile = open(self.familySavePath, "w", encoding="utf-8", newline="")
        # self.familyWriter = csv.writer(self.familyFile)
        f = open("range.txt", "r")
        self.arr = []
        for x in f:
            self.arr.append(int(x.strip()))

    def closed(self, reason):
        self.individualFile.close()
        print("-------> Clossing Individual File")

    def start_requests(self):
        ini_cwd=os.getcwd()
        # for j in range(int('12700'),int('12705'),1):#Changes are to be made here as per booth number of your choice
        for j in range(140):#Changes are to be made here as per booth number of your choice
            if j % 14 == 0:
                if self.individualFile:
                    self.individualFile.close()
                if self.familyFile:
                    self.familyFile.close()
                print("~~~~~~~~~~~~~~~~>>>>>>>>>")

                os.mkdir(str(j))
                os.chdir(ini_cwd+'\\'+str(j))

                self.individualFile = open(self.individualSavePath, "w", encoding="utf-8", newline="")
                self.individualWriter = csv.writer(self.individualFile)

                self.familyFile = open(self.familySavePath, "w", encoding="utf-8", newline="")
                self.familyWriter = csv.writer(self.familyFile)

            for k in range(self.arr[j]):
                stno = format(j+1, "03d") + format(k+1, "03d")
                for i in range(1,4000,1):#Changes are to be made here as per selected range of your choice
                    url='http://www.ceo.kerala.gov.in/searchDetails.html?height=500&width=800&paramValue='+str(stno)+str(i)
                    yield scrapy.Request(url=url, callback=self.parse)
                os.chdir(ini_cwd)
    def parse(self, response):
        # filename=response.url.split('=')
        # filename=filename[len(filename)-1]+'.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        # soup=BeautifulSoup(open(filename,encoding="utf-8"),'lxml')
        # if('Invalid access to the page' in soup.text):
        #     os.remove(filename)        

        soup=BeautifulSoup(response.body,'lxml')
        if('Invalid access to the page' in soup.text):
            return
        trs = soup.find_all("tr")
        idCardNo = trs[0].select('tr > td')[1].get_text()
        nameOfElector = trs[1].select('tr > td')[1].get_text().split("<!")[0].strip()
        age = trs[2].select('tr > td')[1].get_text().strip()
        relationName = trs[3].select('tr > td')[1].get_text().split("<!")[0].strip()
        houseNoName = trs[4].select('tr > td')[1].get_text().split("<!")[0].strip().replace("\xa0", " ")
        serialNo = trs[5].select('tr > td')[1].get_text().strip()
        assemblyConstituency = trs[6].select('tr > td')[1].get_text().split("<!")[0].strip().replace("\xa0", " ")
        booth = trs[7].select('tr > td')[1].get_text().split("<!")[0].strip()
        bloTableData = trs[8].select('tr > td > table > tr')[1].select("td")
        bloDetails = bloTableData[0].get_text().replace('\n', '   ').strip()
        phoneNumbers = bloTableData[1].get_text().strip()
        status = trs[11].select('tr > td')[1].get_text()
        # print(bloDetails, phoneNumbers, status)
        # print(idCardNo, nameOfElector, age, relationName, houseNoName, serialNo, assemblyConstituency, booth, bloDetails, phoneNumbers, status)
        try:
            self.individualWriter.writerow([idCardNo, nameOfElector, age, relationName, houseNoName, serialNo, assemblyConstituency, booth, bloDetails, phoneNumbers, status])
        except Exception as e:
            print("[Individual Write Error]", e)
            # print(idCardNo, nameOfElector, age, relationName, houseNoName, serialNo, assemblyConstituency, booth, bloDetails, phoneNumbers, status)

        if('No data available' in trs[14].text):
            return
        try:
            for tr in trs[14:]:
                tds = tr.select('tr > td')
                fNameOfElector = tds[0].get_text()
                fRelationName = tds[1].get_text()
                fHouseName = tds[2].get_text()
                fSerialNo = tds[3].get_text().strip()
                fLACNo = tds[4].get_text().strip()
                fPSNo = tds[5].get_text().strip()
                fIdCardNo = tds[6].select('td > a')[0].get_text().strip()
                fStatus = tds[7].get_text().strip()
                fPrimaryIdCardNo = idCardNo
                self.familyWriter.writerow([fNameOfElector, fRelationName, fHouseName, fSerialNo, fLACNo, fPSNo, fIdCardNo, fStatus, fPrimaryIdCardNo])
        except Exception as e:
            print("[Family Write Error]", e)
            filename=response.url.split('=')
            filename=filename[len(filename)-1]+'.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)
            soup=BeautifulSoup(open(filename,encoding="utf-8"),'lxml')
            if('Invalid access to the page' in soup.text):
                os.remove(filename)        
if __name__ == "__main__":

    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
