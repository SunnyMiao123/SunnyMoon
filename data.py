import requests
from bs4 import BeautifulSoup

class Hospital:
    def __init__(self):
        self.website=""
        pass
    website="http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8"
    def getHospitalList():
        html=requests.get(Hospital.website).content
        soup=BeautifulSoup(html)
        print(soup)

if __name__ == "__main__":
    Hospital.getHospitalList()