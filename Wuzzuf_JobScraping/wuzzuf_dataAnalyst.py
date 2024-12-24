import csv
from bs4 import BeautifulSoup
import requests
from itertools import zip_longest

job_list = []
company_names_list = []
company_loc_list = []
skills_list = []
links = []
salary = []
id_list=[]
requirments=[]
page_num=0
while True:
    try:
    
        req = requests.get(f'https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q=Data%20Analyst&start={page_num}') 
    
        html_text = req.content
    
        soup = BeautifulSoup(html_text, 'lxml')
        page_limit=int(soup.find('strong').text.strip())

        if(page_num > page_limit//15):
            print("pages ended")
            break         
                


    
     
        job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
        company_names = soup.find_all('a', {'class': 'css-17s97q8'})
        companies_loc = soup.find_all('span', {'class': 'css-5wys0k'})
        skills = soup.find_all('div', {'class': 'css-y4udm8'})

    
        for i in range(len(job_titles)):
            job_list.append(job_titles[i].text.strip())
            link_tag = job_titles[i].find('a')
            if link_tag and link_tag.has_attr('href'):
                links.append(link_tag['href'])
            company_names_list.append(company_names[i].text.strip())
            company_loc_list.append(companies_loc[i].text.strip())
            skills_list.append(skills[i].text.strip())

        salary_elements=[]
        req_elements=[]
   
        for link in links:
                req_n = requests.get(link)
            #print(req_n.status_code)
                html_text_n = req_n.content
                soup_n = BeautifulSoup(html_text_n, 'lxml')
                #print(soup_n.prettify())
                break
                salary_elements=soup_n.find('div' ,{'class':'css-rcl8e5'})
                #print(salary_elements)  
                req_elements=soup_n.find('div' ,{'class':'css-1t5f0fr'}).ul
                #print(req_elements)
            
                #if salary_element:
                    #salary.append(salary_element.text.strip())
                #if req_element:
                    #requirments.append(req_element.text.strip())
        page_num+=1
        print('page switched')
    except Exception as e:
         print(f"Error catched:{e}")

 # Set ids
for j in range(page_limit):
     id_list.append(j)
 
with open(r"D:\Data_AnalystJobs.csv", "w", newline='', encoding='utf-8') as my_files:
    db = csv.writer(my_files)
    db.writerow(['ID','Job Titles', 'Company Names', 'Locations', 'Skills'])
   
    for I_D, job, company, loc, skill in zip_longest(id_list,job_list, company_names_list, company_loc_list, skills_list):
        db.writerow([I_D,job, company, loc, skill])
