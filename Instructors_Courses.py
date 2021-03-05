from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

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
    driver = webdriver.Chrome("C:/Users/Zubier/Desktop/UAlberta-North_DB/chromedriver.exe")
    return driver


def getCourses(driver):
    uAlberta_courses = []
    for each_keyword in facultyList:
        each_keyword = f'"{each_keyword[1]}"'
        driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&t=Courses&sort=relevancy")
        time.sleep(.5)
        # wait for the element to load
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))
        except TimeoutException:
            # print("TimeoutException: Element not found")
            continue
            # return None

        # Step 2: Create a parse tree of page sources after searching
        soup = BeautifulSoup(driver.page_source, "lxml")
        numofPages = soup.select(".CoveoQuerySummary > span:nth-child(1) > span:nth-child(2)")
        result = numofPages[0].text

        for index in range(int(int(result)/10)+1):
            driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&first={index*10}&t=Courses&sort=relevancy")
            time.sleep(.5)
            # wait for the element to load
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))     
            except TimeoutException:
                # print("TimeoutException: Element not found")
                return None
                    
            soup = BeautifulSoup(driver.page_source, "lxml")
            # Step 3: Iterate over the search result and fetch the course
            for course_page in soup.select("div.CoveoResult"):
                for course in course_page.find_all('a'):
                    course_num1 = Course()
                    # course_num1.title = course.text
                    course_num1.url = course.get('href')
                    uAlberta_courses.append(course_num1)

    course = 0
    for course in uAlberta_courses:
        driver.get(course.url)
        time.sleep(.5)
        f = open('test.csv',"a")
        soup = BeautifulSoup(driver.page_source, "lxml")
        faculty_description = soup.select('div.pb-2:nth-child(3) > p:nth-child(3) > a:nth-child(1)')
        course.faculty = faculty_description[0].text.strip()
        course_description = soup.h2
        course_description = course_description.text.strip()
        course_description = f'"{course_description}"'
        course_url = f'"{course.url}"'
        
        for faculty_course_description_instructor in soup.select("div.content:nth-child(4)"):
            for every_faculty_course_description in faculty_course_description_instructor.find_all('div', attrs={'class': 'card mt-4 dv-card-flat'}):    
                course_description_term = every_faculty_course_description.h4.string
                for every_course_description_term in every_faculty_course_description.find_all('div',attrs={'class': 'col-lg-4 col-12 pb-3'}):
                    try:
                        course_description_type = f'"{every_course_description_term.strong.text.strip()}"'
                    except AttributeError:
                        course_description_type = f'"{"N/A"}"'
                    # course_description_date = '"'+every_course_description_term.em.text.strip().split('\n')+'"'
                    course_description_date = every_course_description_term.em.text.strip().split('\n')
                    if len(course_description_date) > 1:
                        course_description_time = '"'+course_description_date[1]+'"'
                    else:
                        course_description_time = f'"{"N/A"}"'
                    course_description_date = '"'+course_description_date[0]+'"'

                    

                    try:
                        course_prof = every_course_description_term.find_all('a')
                        if len(course_prof) == 2:
                            course_prof = course_prof[1].text.strip()
                        else:
                            course_prof = course_prof[0].text.strip()
                    except IndexError:
                        course_prof = f'"{"N/A"}"'
                    for each_instructor in facultyList:
                        if course_prof == each_instructor[1]: 
                            course_prof = f'"{course_prof}"'         
                            final_string = course_description+',' + course_url + "," + course_description_term + "," + course_description_type + "," + course_description_date + "," + course_description_time + "," +  course_prof 
                            final_string1 = final_string + "\n"
                        elif course_prof != each_instructor[1]:
                            continue
                        else:
                            course_prof = f'"{course_prof}"' 
                            print(course_prof) 
                            final_string = course_description+',' + course_url + "," +course_description_term + "," + course_description_type + "," + course_description_date + "," + course_description_time +  "," + course_prof 
                            final_string1 = final_string + "\n"
                    f.write(final_string1)

# create the driver object.
driver = configure_driver()
with open("./Faculty_Members.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 
facultyList = []
for word in content:
    word = word.split(" - ")
    facultyList.append(word)
for eachIndex in facultyList:
    search_faculty = eachIndex[0]
    search_keyword = eachIndex[1]
getCourses(driver)
# close the driver.
driver.close()


