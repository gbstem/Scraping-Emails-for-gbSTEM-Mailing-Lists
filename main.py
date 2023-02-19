from bs4 import BeautifulSoup

def retrieve_info(filename, public = True):
  with open(filename, 'r') as html_file:
    content = html_file.read()
  
    #get school name
    html = BeautifulSoup(content, 'lxml')
  
    #get schools
    schoolshtml = html.find_all('span', class_ = 'lg')
    schools = [s.text for s in schoolshtml]
    if public:
      schools = [s[s.index(":")+2:] for s in schools]
    else: 
      schools = [s[s.index(".")+2:] for s in schools]
    schools = [s[:s.index("(")-1] for s in schools]
  
    #get principals
    principalhtml = html.find_all('td', class_ = 'searchindent')
    principals = [p.text[p.text.index(":")+2:p.text.index("""
      """)] for p in principalhtml]
  
    #get emails
    emailshtml = html.find_all('td', class_ = 'right')
    emails = [e.find('a').text for e in emailshtml if e.find('a')!= None]

    return list(zip(schools, principals, emails))

import pandas as pd
instructorschools = pd.DataFrame(retrieve_info('privateschools(instructors).html',False) + retrieve_info('publicschools(instructors).html'), columns=['schools', 'principals', 'emails'])
instructorschools.to_csv('instructorschools.csv', index=False)

studentschools = pd.DataFrame(retrieve_info('privateschools(students).html',False) + retrieve_info('publicschools(students).html'), columns=['schools', 'principals', 'emails'])
studentschools.to_csv('studentschools.csv', index=False)
    
  