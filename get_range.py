import requests
import json


lacs = [5, 16, 19, 32, 48, 60, 73, 87, 92, 101, 110, 115, 126, 140]

url = "http://www.ceo.kerala.gov.in/electoralroll/partsListAjax.html?currentYear=2020&distNo={0}&lacNo={1}&sEcho=1&iColumns=4&sColumns=&iDisplayStart=0&iDisplayLength=10&iSortingCols=1&iSortCol_0=0&sSortDir_0=asc&bSortable_0=false&bSortable_1=false&bSortable_2=false&bSortable_3=false&undefined=undefined"
arr = []
for i in range(14):
    district = i + 1
    st = 0
    if i > 0:
        st = lacs[i-1]

    for j in range(st+1, lacs[i]+1):
        x = requests.get(url.format(district, j))
        data = json.loads(x.text)
        print(district, j, data['iTotalDisplayRecords'])
        arr.append(data['iTotalDisplayRecords'])
    print('-----')
print('-------------------------------')
for ar in arr:
    print(ar)
