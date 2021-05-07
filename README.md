**_Update Date : April 30,2020_**
**_Zubier Hagi (Hagi@ualberta.ca)_**

## Setup ##

-- Please follow the details below as they will be required to have the program run successfully. --

**Required dependencies:**

`— Web Browser: Google Chrome`
`— Chrome Driver`

`— Beautifulsoup4`
`— Selenium`
`— Google Docs API`
`— Google oAuth2`

`— Dotenv`
`— Code Editor`
`— Python3.4+`


**ChromeDriver:**
WebDriver is an open source tool for automated testing of webapps across many browsers. It provides capabilities for navigating to web pages, user input, JavaScript execution, and more.  ChromeDriver is a standalone server that implements the W3C WebDriver standard. ChromeDriver is available for Chrome on Android and Chrome on Desktop (Mac, Linux, Windows and ChromeOS).  


**Beautifulsoup:4**
Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.#

**Selenium:**
The selenium package is used to automate web browser interaction from Python. #


**Google Docs API:**
A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to Create a project and enable the API #

**Google oAuth2:**
This library provides the ability to authenticate to Google APIs using various methods. It also provides integration with several HTTP libraries.#

**Dotenv:**
Dotenv is a zero-dependency module that loads environment variables from a .env file into process.env. Storing configuration in the environment separate from code is based on The Twelve-Factor App methodology.#


## Installation Guide ##
1) Download Google Chrome if not already installed:

    https://www.google.com/chrome/

2) Download the latest stable released Chrome Driver for the correct OS:

    https://chromedriver.chromium.org/

3) Download one of the following Code Editors:

    Visual Studio Code by Microsoft, Atom or Sublime Text
    
        https://code.visualstudio.com/
        
        https://atom.io/
        
        https://www.sublimetext.com/

4) Download the latest version of Python3 for the correct OS (Operating System):

    https://www.python.org/downloads/

5) Download the source code file or clone the GitHub repository. 

6) Open the downloaded source code file within the code editor.

7) Within the Terminal command, download the following dependencies as followed:

   `pip3 install beautifulsoup4`
    
   `pip3 install -U selenium`
    
   `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
    
   `pip3 install3 --upgrade google-auth`
    
   `pip3 install google-auth google-auth-oauthlib`
    
   `pip3 install python-dotenv`
    
   `pip3 install dotenv`

8) You should then be able to run the intended file to accomplish the required tasks.

    Faculty_Members.txt: A list of Northern Instructors. It's important to note the format “Faculty — First Name Last Name”.

    Northern_Instructor_Reserach_Courses.py: Obtains a list of *research* related course that in relation to the list of Northern Instructor from Faculty_Members.txt.
    
    Instructors_Courses.py: Obtains a list of all courses that are in relation to the Northern Instructor from Faculty_Members.txt.

    Instructors_Courses.py: Obtains courses of keywords that have a relation to a Northern based course.

    chromedriver.exe: Chrome extension for web automation.

    .env: Contains API Key that contains extremely important information which should not be anywhere shared publicly. 

    keys.json: Contains Google Cloud API keys, for authentication works within the Google Cloud as a service account. This is also extremely important information which should not be anywhere shared publicly.

9) Please ensure that you don't close or interrupt the Google Chrome driver as the automation is in progress. You will be able to distinguish the different type of Chrome window/browser with the disclaimer within the header of the window.

10) The updated data can be found within the Google Drive (Google Sheets) in correspondence with its correct sheet name.


## Future Updates Guide ## 

    The Google Web Browser often is updated automatically by Google. This may cause issues in the future with the Chrome Driver extension. Though this can be easily fixed by doing the following steps:

    Check the version of the Google Chrome: Within the Google Chrome find Help > About Google Chrome.
    
    Remove the current chromedriver.exe within this folder
    
    Redownload the latest Chrome Driver and replace the removed Chrome Driver extension with the new one.
