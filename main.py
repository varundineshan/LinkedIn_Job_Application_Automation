from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import re
class LinkedInAutomate:

    def __init__(self,data):
        self.email=data['email']
        self.password=data['password']
        self.keywords=data['keywords']
        self.location=data['location']
        self.driver=webdriver.Chrome(data['driver_path'])

    def login(self):
        self.driver.maximize_window()
        #provide path for login page
        self.driver.get("https://www.linkedin.com/login")
        
        emailField=self.driver.find_element_by_name("session_key")
        emailField.clear()
        emailField.send_keys(self.email)

        passField=self.driver.find_element_by_name("session_password")
        passField.clear()
        passField.send_keys(self.password)
        passField.send_keys(Keys.RETURN)
    
    def job_click(self):
        job=self.driver.find_element_by_link_text('Jobs').click()
        time.sleep(2)
        searches=self.driver.find_element_by_xpath("(//input[@role='combobox'])[1]")
        searches.clear()
        searches.send_keys(self.keywords)

        location=self.driver.find_element_by_xpath("(//input[@role='combobox'])[2]")
        location.clear()
        location.send_keys(self.location)
        location.send_keys(Keys.RETURN)

    def job_filter(self):
        time.sleep(2)
        #clicking on all filters button
        filter = self.driver.find_element_by_xpath("//button[@aria-label='All filters']").click()    
        time.sleep(1)
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-experience-1']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-experience-2']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-experience-3']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-experience-4']").click()
        
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-jobType-F']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-jobType-C']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-jobType-T']").click()
        filter = self.driver.find_element_by_xpath("//label[@for='advanced-filter-jobType-I']").click()
        #ActionChains(self.driver).move_to_element(filter).click().perform()
        
        time.sleep(1)
        filter = self.driver.find_element_by_xpath("//button[@aria-label='Apply current filters to show results']").click()

        time.sleep(2)
        filter = self.driver.find_element_by_xpath("//button[@aria-label='Easy Apply filter.']").click() 
    
    def job_apply_list_click(self):
        #finding no of results
        results=self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        results=int(results.text.split(' ',1)[0].replace(",",""))
        print(results)

        time.sleep(2)
        page=self.driver.current_url
        list_of_pages=self.driver.find_elements_by_class_name('full-width.artdeco-entity-lockup__title.ember-view')
        #//a[@class="disabled.ember-view.job-card-container__link job-card-list__title"]

        print("selected titles")
        
        for lst in list_of_pages:
            hover=ActionChains(self.driver).move_to_element(lst)
            hover.perform()
            time.sleep(1)
            titles = lst.find_elements_by_class_name('disabled.ember-view.job-card-container__link.job-card-list__title')
            for title in titles:
                time.sleep(3)
                title.click()
                self.job_submision(title)

    def job_submision(self,job):
        time.sleep(2)

        try:
            apply_button=self.driver.find_element_by_xpath("//button[@data-control-name='jobdetails_topcard_inapply']")       
            apply_button.click()
        except NoSuchElementException:
            print("already applied")
        time.sleep(1)

        try:
            print("reached clicking next-------------------------------------------------------------")
            click_next=self.driver.find_element_by_xpath("//button[@data-control-name='submit_unify']")
            click_next.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            print('This is not direct application, moving to next')
            try:
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element_by_xpath("//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

    def session_exit(self):
        self.driver.close()            

    def do_work(self):
        varlock.login()
        time.sleep(2)
        varlock.job_click()
        time.sleep(1)
        varlock.job_filter()
        time.sleep(1)
        varlock.job_apply_list_click()
        time.sleep(4)
        varlock.session_exit()
        
if __name__ == '__main__':
    with open('config.json') as cfile:
        data=json.load(cfile)
    varlock=LinkedInAutomate(data)
    varlock.do_work()
    