from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import os
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

class Course:
    # def __init__(self):
    pass

def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    driver = webdriver.Chrome("..\chromedriver.exe")
    
    # Google Spreedsheets!!!
    SERVICE_ACCOUNT_FILE = "keys.json"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID_KEY = '1Hmpii8-wu2n4dyjizmsVXmQ3PsxuEZexZNlsM7z4Fj8'
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().clear(spreadsheetId=SPREADSHEET_ID_KEY, range="Northern Courses!A:N").execute()
    headerInfo = [["Course Number","Course Title","Course Description","Course Link","Faculty","Term","Course Type","Course Duration","Course Time","Instructor First Name","Instructor Last Name","Instructor Profile"]]
    # Call the Sheets API
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID_KEY,
                                range="Northern Courses!A1", valueInputOption="USER_ENTERED",body={"values":headerInfo}).execute()
    return driver

# Thus functions parses and captures any of the available courses that each instructor teaches.
def getCourses(driver):
    # Step 1: instantiates a list of uAlberta_Courses to store the parsed courses
    uAlberta_courses = []
    for each_keyword in search_keyword:
        if type(each_keyword) == list:
            each_keyword = f'"{each_keyword[0]}"' +  each_keyword[1]
            each_keyword = str(each_keyword)
        else:
            each_keyword = f'"{each_keyword}"'
        driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&t=Courses&sort=relevancy")
        time.sleep(.5)
        # wait for the element to load
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))     
        except TimeoutException:
            print("TimeoutException: Element not found")
            continue
            # return None

        # Step 2: Create a parse tree of page sources after searching
        soup = BeautifulSoup(driver.page_source, "lxml")
        numofPages = soup.select("span.coveo-highlight:nth-child(3)")
        result = numofPages[0].text
        try:
            result = math.ceil(float(result)/10)
        except ValueError:
            numofPages = soup.select("span.coveo-highlight:nth-child(2)")
            result = numofPages[0].text
            result = math.ceil(float(result)/10)


        for index in range(result):
            driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&first={index*10}&t=Courses&sort=relevancy")
            time.sleep(.5)
            # wait for the element to load
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))     
            except TimeoutException:
                print("TimeoutException: Element not found")
                return None
                    
            soup = BeautifulSoup(driver.page_source, "lxml")
            # Step 3: Iterate over the search result and fetch the course
            for course_page in soup.select("div.CoveoResult"):
                for course in course_page.find_all('a'):
                    course_num1 = Course()
                    course_num1.url = course.get('href')
                    course_num1.tit = each_keyword
                    uAlberta_courses.append(course_num1)
                    
    # Step 4: Parses through each course obtained to it's respectful variable and validates any empty values
    course = 0
    for course in uAlberta_courses:
        driver.get(course.url)
        time.sleep(.5)
        # f = open('Northern Courses.csv',"a")
        soup = BeautifulSoup(driver.page_source, "lxml")
        faculty_type = soup.select('div.pb-2:nth-child(3) > p:nth-child(3) > a:nth-child(1)')
        course_details = soup.select('div.pb-2:nth-child(3) > p:nth-child(4)')
        if len(course_details) == 0:
            course_description = "N/A"
        else:
            course_description = course_details[0].text.strip()
        course.faculty = faculty_type[0].text.strip()
        course_Info = soup.h2
        course_Info = course_Info.text.strip()
        course_Info = f"{course_Info}"
        course_url = f"{course.url}"
        course_faculty = f"{course.faculty}"
        course_number = course_Info.split(" - ", 1)[0]
        course_title = course_Info.split(" - ", 1)[1]


        for faculty_course_description_instructor in soup.select("body"):
            for every_course_description_term in faculty_course_description_instructor.find_all('div', attrs={'class': 'card mt-4 dv-card-flat'}): 
                course_description_term = every_course_description_term.h4.string 
                course_description_type = every_course_description_term.strong.text.strip()
                
                for course_term_description_type in every_course_description_term.find_all('div', attrs={'class': 'col-lg-4 col-12 pb-3'}):
                    course_description_type = course_term_description_type.strong.text.strip()
                    
                    if len(course_term_description_type.findAll('em')) >= 2:
                        course_description_capacity = course_term_description_type.findAll('em')[0]
                        course_description_date = course_term_description_type.findAll('em')[1].text.strip().split('\n')
                    course_prof = course_term_description_type.find_all('a')
                    
                    if len(course_description_date) > 1:
                            course_description_time = course_description_date[1]
                            course_description_date = course_description_date[0]
                    else:
                        course_description_time = "N/A"
                        course_description_date = course_description_date[0]

   
                    if len(course_prof) >= 1:
                        for course_profInfo in range(len(course_prof)):
                            course_proflink = 'https://apps.ualberta.ca/directory/person/' + str(course_prof[course_profInfo].get('href').rsplit('/', 1)[-1])
                            course_profInfo = course_prof[course_profInfo].text.strip()
                            course_profName = course_profInfo
                            if course_profName == '':
                                pass
                            else:
                                course_firstName = course_profName.split(" ", 1)[0]
                                course_lastName = course_profName.split(" ", 1)[1]

                                if course.faculty not in search_faculty:
                                    course_faculty = f"{course.faculty}"
                                    final_string = f'"{course_number}"'+","+f'"{course_title}"'+","+f'"{course_description}"'+","+f'"{course_url}"'+","+f'"{course.faculty}"'+ ","+f'"{course_description_term}"'+","+f'"{course_description_type}"'+","+f'"{course_description_date}"'+","+f'"{course_description_time}"'+","+f'"{course_profName}"'+","+f'"{course_proflink}"'
                                    spreedsheetlist = ''
                                    final_content = (str(final_string) + "\n")
                                    
                                else:
                                    course_faculty = f"{course.faculty}"
                                    final_string = f'"{course_number}"'+","+f'"{course_title}"'+","+f'"{course_description}"'+","+f'"{course_url}"'+","+f'"{course.faculty}"'+ ","+f'"{course_description_term}"'+","+f'"{course_description_type}"'+","+f'"{course_description_date}"'+","+f'"{course_description_time}"'+","+f'"{course_profName}"'+","+f'"{course_proflink}"'
                                    final_content = (str(final_string) + "\n")
                                    spreedsheetlist = [[course_number,course_title,course_description,course_url,course_faculty,course_description_term,course_description_type,course_description_date,course_description_time,course_firstName,course_lastName,course_proflink]]
                                
                                # Step 5: Outputs the finalized data into the sheet
                                time.sleep(1)
                                if spreedsheetlist != '':
                                    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID_KEY,
                                                range="Northern Courses!A2", valueInputOption="USER_ENTERED",body={"values":spreedsheetlist}).execute()
                                else:
                                    continue

                    else:
                        course_profName =  "N/A"
                        course_proflink = "N/A"
                        course_firstName = course_profName
                        course_lastName = course_profName

                        if course.faculty not in search_faculty:
                            course_faculty = f"{course.faculty}"
                            final_string = f'"{course_number}"'+","+f'"{course_title}"'+","+f'"{course_description}"'+","+f'"{course_url}"'+","+f'"{course.faculty}"'+ ","+f'"{course_description_term}"'+","+f'"{course_description_type}"'+","+f'"{course_description_date}"'+","+f'"{course_description_time}"'+","+f'"{course_profName}"'+","+f'"{course_proflink}"'
                            final_content = (str(final_string) + "\n")
                            spreedsheetlist = ''

                        else:
                            course_faculty = f"{course.faculty}"
                            final_string = f'"{course_number}"'+","+f'"{course_title}"'+","+f'"{course_description}"'+","+f'"{course_url}"'+","+f'"{course.faculty}"'+ ","+f'"{course_description_term}"'+","+f'"{course_description_type}"'+","+f'"{course_description_date}"'+","+f'"{course_description_time}"'+","+f'"{course_profName}"'+","+f'"{course_proflink}"'
                            final_content = (str(final_string) + "\n")
                            spreedsheetlist = [[course_number,course_title,course_description,course_url,course_faculty,course_description_term,course_description_type,course_description_date,course_description_time,course_firstName,course_lastName,course_proflink]]
                        
                        # Step 5: Outputs the finalized data into the sheet
                        time.sleep(1)
                        if spreedsheetlist != '':
                            result = sheet.values().append(spreadsheetId=SPREADSHEET_ID_KEY,
                                            range="Northern Courses!A2", valueInputOption="USER_ENTERED",body={"values":spreedsheetlist}).execute()
                        else:
                            continue

# create the driver object.
load_dotenv()
SPREADSHEET_ID_KEY = os.getenv('SPREADSHEET_ID_API_KEY')
driver = configure_driver()

# Applicable keywords to search, 
# Validation of keywords that need to not be duplicated/required are considered and removed from query search
search_keyword = [["Aboriginal",f'-"Indigenous Legal Issues"'],"Arctic",["Boreal","-Arctic"],["circumpolar","-Boreal"],"Canada's North","climate and weather","Cree",["Indigenous peoples",f'-"Native Peoples"'],["Native Peoples","-Aboriginal"],["Native Studies",f'-"Indigenous"'],["Northern",f'-"Northern Regions"'f'-"North"'f'-"Northern Ecosystems"'f'-"Northern Ecology"'],"Northern Regions",["northern systems",f'-"Northern"'],
                    ["Polar", "-Calculus"],"permafrost","ice fields","ice masses","ice age",["traditional knowledge",f'-"environmental sustainability"'],["Yukon",f'-"Canadian North"'],"Northwest Territories","NWT","Nunavik","Nunatsiavut","cryosphere",["tundra",f'-" Northern Ecosystems"'],"Indigenous languages","Indigenous health","Indigenous wellbeing","wildlife management","land claims","northern education","Indigenous education",
                        "Participatory Research","Advanced Research Skills"]

# Applicable faculties to search within
search_faculty = ["Faculty of Agricultural, Life and Environmental Sciences","Faculty of Arts","Augustana Faculty","Faculty of Engineering","Faculty of Education","Faculty of Kinesiology, Sport, and Recreation","Faculty of Law","Faculty of Native Studies","Faculty of Public Health","School of Public Health","Faculty of Science"]

# Instantiation Google API authentication 
SERVICE_ACCOUNT_FILE = "keys.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
getCourses(driver)
# close the driver.
driver.close()