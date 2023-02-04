from bs4 import BeautifulSoup
import json

import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw() 
#Answer Key
print('Upload you answer key as a webpage file with .aspx')
answer_key = filedialog.askopenfilename()
with open(answer_key) as f:
    soup = BeautifulSoup(f, "html.parser")
table = soup.find("table", {"id": "ctl00_LoginContent_grAnswerKey"})
data = []
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        data.append([cell.text for cell in cells])
key = {}
for arr in data:
    key[arr[2].strip('\n')] = arr[3].strip('\n')
    

#Response_Sheet
print('Upload you response_sheet as a webpage file with .html')
response_sheet = filedialog.askopenfilename()
with open(response_sheet) as f:
    soup = BeautifulSoup(f, "html.parser")
tables = soup.find_all("table", {"class": "menu-tbl"})
values = {}
data = []
for table in tables:
    sub = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            sub.extend([cell.text for cell in cells])
    data.append(sub)
answers = []
tables = soup.find_all("table",{"class": "questionRowTbl"})
for table in tables:
    sub = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            sub.extend([cell.text for cell in cells])
    answers.append(sub)
counter = 0
for question in data:
    if 'MCQ' in question and 'Answered' in question:
        chosen = int(question[15])
        question_id = question[3]
        answer_id = question[3+chosen*2]
        values[question_id] = answer_id
    if 'SA' in question:
        answer = answers[counter]
        if 'Answered' in question:
            question_id = question[3]
            answer_id = answer[5]
            values[question_id] = answer_id
    counter += 1

#Calculate Score
correct = 0
incorrect = 0
corr_q = []
incorr_q = []
for elem in values:
    if(key[elem] == values[elem]):
        correct+= 1
        corr_q.append(elem)
    else:
        incorrect += 1
        incorr_q.append(elem)
total = correct*4 - incorrect
print('----------------------------------------')
print('You attempted: ' + str(correct+incorrect) + ' questions')
print('You got ' + str(correct) + ' correct')
print('You got ' + str(incorrect) + ' incorrect')
print('Your total score is: ' + str(total))
print('----------------------------------------')
print('Correct Questions: ')
for q in corr_q:
    print(q)
print('----------------------------------------')
print('Incorrect Questions: ')
for q in incorr_q:
    print(q)
input()