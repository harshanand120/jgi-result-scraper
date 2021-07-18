from bs4 import BeautifulSoup
import requests
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

subjects=list()
def get_result(usn):
    print(usn)
    def arranngeMarks(subMark,fail=False):
        if fail:
            marks={'sl_no':None,
                'subject':None,
                'internal_marks':None,
                'exam_marks':None,
                'practical_marks':None,
                'total':None,
                'credits':None,
                'grade':None
        }
        else:
            x=subMark.findAll('td')
            marks={'sl_no':x[0].span.text,
                'subject':x[1].span.text,
                'internal_marks':x[2].span.text,
                'exam_marks':x[3].span.text,
                'practical_marks':x[4].span.text,
                'total':x[5].span.text,
                'credits':x[6].span.text,
                'grade':x[7].span.text
        }
        return marks
    try:
        r=requests.Session()

        s1=r.get("https://results.jainuniversity.ac.in/webResult.aspx")
        html1=BeautifulSoup(s1.text,'html.parser')
        viewstate = html1.find(id="__VIEWSTATE").attrs["value"]
        viewstategenerator = html1.find(id="__VIEWSTATEGENERATOR").attrs["value"]
        eventvalidation = html1.find(id="__EVENTVALIDATION").attrs["value"]

        headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control":"max-age=0",
        "content-length":"760",
        "content-type":"application/x-www-form-urlencoded",
        "origin":"https://results.jainuniversity.ac.in",
        "referer":"https://results.jainuniversity.ac.in/webResult.aspx?id=UG&value=Current",
        "sec-ch-ua-mobile":"?0",
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",
        "sec-fetch-site":"same-origin",
        "sec-fetch-user":"?1",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
        data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator,"__EVENTVALIDATION":eventvalidation,"txtStudentCode":usn,"btnGetResult":"Show Result"}
        s2=r.post("https://results.jainuniversity.ac.in/webResult.aspx",verify=False,headers=headers,data=data)
        soup=BeautifulSoup(s2.text,'html.parser')
        name=soup.find('span',attrs={'id':'lblStuName'}).text
        result=soup.find('span',attrs={'id':'lblResult'}).text
        total=soup.find('span',attrs={'id':'lblTotalMarks'}).text
        sgpa=soup.find('span',attrs={'id':'lblSGPA'}).text
        marks_table = soup.find("table",attrs={"id":"gdResultDetails"})
        headings = [x.text for x in marks_table.find('thead').find('tr').findAll('th')]
        marks = [x for x in marks_table.tbody.findAll('tr')]
        extracted_marks = []
        global subjects
        subjects=[]
        for x in marks:
            subjects.append(x.findAll('td')[1].span.text)
        extracted_marks.append({'usn':usn,'name':name,'result':result,'total':total,'sgpa':sgpa})
        for x in marks:
            extracted_marks.append(arranngeMarks(x))     
        return extracted_marks
    except Exception as e:
        extracted_marks = []
        name=None
        result=None
        total=None
        sgpa=None
        extracted_marks.append({'name':name,'result':result,'total':total,'sgpa':sgpa})
        extracted_marks.append(arranngeMarks('',fail=True))
        return extracted_marks

usn = input("Enter usn prefix (eg. 18btran):  ")
limit = int(input("Enter upper limit:  "))+1
class_mark=[]

if limit<10:
    for x in range(1,limit):
        class_mark.append(get_result(f'{usn}00{x}'))
else:
    for x in range(1,10):
        class_mark.append(get_result(f'{usn}00{x}'))
if limit>99:
    for x in range(10,100):
        class_mark.append(get_result(f'{usn}0{x}'))
    for x in range(100,limit):
        class_mark.append(get_result(f'{usn}{x}'))
else:
    for x in range(10,limit):
        class_mark.append(get_result(f'{usn}0{x}'))

# print(class_mark)
submark_only=[]
temp=[]
for x in ['usn','name','result','total','sgpa']:
    temp.append(x)
for x in subjects:
    temp.append(x)
submark_only.append(temp)
for x in class_mark:
    temp=[]
    for g in x[0].keys():
        temp.append(x[0][g])
    for y in x[1:]:
        type(print(y))
        temp.append(y['total'])
    submark_only.append(temp)


line=''
for x in submark_only:
    for y in x:
        line+=str(y)
        line+=','
    line=line[:-1]+'\n'
# print(line)

i=input('Filename (csv): ')
with open(i,'w+') as f:
    f.write(line)
