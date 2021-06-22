#Importing libraries - 
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

#Document Load : 

driver=webdriver.Chrome('C:\\Users\\nihal\\Desktop\\Python\\chromedriver.exe')

def html_text(url):
    driver.get(url)
    time.sleep(3)
    
    #Step 2 - Parsing : 
    soup = BeautifulSoup(driver.page_source,'html.parser')
    return soup


#Each page contains 20 job results. For each job we will scrape the role,company,
# location, experience, skills, salary, freshness and the link to get more info
# about the job.


#Creating a dictionary for storing the information after scraping
job_list={"Job Title":[],
          "Company Name":[],
          "Experience":[],
          "Salary":[],
          "Locations":[],
          "Skills Required":[],
          "Freshness":[],
          "More Info at":[]}


#Extraction of job details and appending into the dictionary - 
def extract_job(job):
    title=job.find('a',class_ ='title fw500 ellipsis').text
    
    company=job.find('a',class_ ='subTitle ellipsis fleft').text    
    
    experience=job.find('li',class_ ='fleft grey-text br2 placeHolderLi experience')
    if experience == None:
        experience='Not mentioned'
    else:
        experience = experience.text
    
    salary=job.find('li',class_ ='fleft grey-text br2 placeHolderLi salary').text
    
    location=job.find('li',class_ ='fleft grey-text br2 placeHolderLi location').text
    
    skills=job.find_all('li',class_ ='fleft fs12 grey-text lh16 dot')
    skill_list=[skill.text for skill in skills]
    
    freshness=job.find('div',class_ ='type br2 fleft grey')
    if freshness == None :
        freshness=job.find('div',class_ ='type br2 fleft green').text
    else:
        freshness=freshness.text
   
    more_info=job.div.a['href']    
    
    
    job_list['Job Title'].append(title)
    job_list['Company Name'].append(company)
    job_list['Experience'].append(experience)
    job_list['Salary'].append(salary)
    job_list['Locations'].append(location)
    job_list['Skills Required'].append(skill_list)
    job_list['Freshness'].append(freshness)    
    job_list['More Info at'].append(more_info)
     

#Function to get the url of each webpage -
def get_url(n):
    if n == 1:
        url='https://www.naukri.com/data-science-jobs?k=data%20science'
    else:
        url='https://www.naukri.com/data-science-jobs-{}?k=data/%20science'
        url=url.format(n)
    return url

#Extracting job details from multiple pages and appending into the dictionary -
start_page=1
end_page= 50
for page in range(start_page,end_page+1):
    page_url = get_url(page)
    soup_of_page =html_text(page_url)
    jobs = soup_of_page.find_all('article',class_ ='jobTuple bgWhite br4 mb-8')
    for job in jobs:
        extract_job(job)

driver.close()


#Creating a dataframe from dictionary - 
jobs_df=pd.DataFrame(job_list)
print(jobs_df.tail(5))

#Creating a CSV file - 
jobs_df.to_csv("Data_Science_Jobs.csv",index=False)

