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
    driver = webdriver.Chrome("C:/Users/Zubier/Desktop/UAlberta-North/UAlberta/chromedriver.exe")
    return driver

def getCourses(driver):
    uAlberta_courses = []
    uAlberta_Northern_courses = []
    # search_faculty = ["Faculty of Agricultural, Life and Environmental Sciences", "Faculty of Science"]
    # Step 1: Go to pluralsight.com, category section with selected search keyword.

    for each_keyword in search_keyword:
        driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&t=Courses&sort=relevancy")
        time.sleep(.5)
        # wait for the element to load
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))
            
        except TimeoutException:
            print("TimeoutException: Element not found")
            return None

        # Step 2: Create a parse tree of page sources after searching
        soup = BeautifulSoup(driver.page_source, "lxml")
        numofPages = soup.select(".CoveoQuerySummary > span:nth-child(1) > span:nth-child(2)")
        result = numofPages[0].text
        # print(result)

        for index in range(int(int(result)/10)+1):
            driver.get(f"https://www.ualberta.ca/search/index.html#q={each_keyword}&first={index*10}&t=Courses&sort=relevancy")
            time.sleep(.5)
            print(index,"/",int(int(result)/10)+1)
            # wait for the element to load
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.coveo-list-layout:nth-child(1)")))     
            except TimeoutException:
                print("TimeoutException: Element not found")
                return None
                    
            soup = BeautifulSoup(driver.page_source, "lxml")
            # Step 3: Iterate over the search result and fetch the course
            for course_page in soup.select("div.CoveoResult"):
                for course in course_page.find_all('a'):
                    # print(course)
                    # for link in course.find_all('')
                    course_num1 = Course()
                    course_num1.title = course.text
                    course_num1.url = course.get('href')
                    uAlberta_courses.append(course_num1)

    # print(uAlberta_courses)
    course = 0
    for course in uAlberta_courses:
        driver.get(course.url)
        time.sleep(.5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        faculty_description = soup.select('div.pb-2:nth-child(3) > p:nth-child(3) > a:nth-child(1)')
        course.faculty = faculty_description[0].text.strip()
        if course.faculty in search_faculty:
            if len(uAlberta_Northern_courses) == 0:
                uAlberta_Northern_courses.append(course)
            else:
                duplicate_found = False
                for northernCourse in uAlberta_Northern_courses:
                    if course.title == northernCourse.title:
                        duplicate_found = True
                        break
                if duplicate_found == False:
                    uAlberta_Northern_courses.append(course)
            

        course_description = soup.select('div.pb-2:nth-child(3) > p:nth-child(4)')
        if len(course_description) == 0:
                course.description = 'There is no available course description.'
        else:
                course.description = course_description[0].text.strip()



    for val in uAlberta_Northern_courses:
        print(val.title,val.faculty)
        

# create the driver object.
driver = configure_driver()
search_keyword = ["Arctic", "circumpolar","Northern region","Canadian north","Canada's north","Northern courses","Northern landscape","northern systems","indigenous peoples"]
search_faculty = ["Faculty of Agricultural, Life and Environmental Sciences", "Faculty of Science"]
getCourses(driver)
# close the driver.
driver.close()