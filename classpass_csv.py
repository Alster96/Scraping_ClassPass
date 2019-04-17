from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv

#initialize the chrome browser
driver = webdriver.Chrome()
#go to the class pass page we want to scrape
driver.get("https://classpass.com/search/new-york/fitness-classes/5hEHUSFYmb5")

#find the username and password fields
username = driver.find_element_by_id("email_field")
password = driver.find_element_by_id("password_field")
#input the user specific infomation
username.send_keys("nycdsa.project1@gmail.com")
password.send_keys("nycdsaproj1")
#log into the website
driver.find_element_by_xpath('//button[@type="submit"]').click()

print("We're in!!")


csv_file = open('classpass.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(["Title", "Instructor", "Rating","Reviews","Time","Duration","Venue","Location","Tags","Price"])

# Page index used to keep track of where we are.
index = -1
while index <=1:
	try:
		print("Page " + str(index+2) + " " + "getting scraped baby!")
		index = index + 1
		# Find all the classes on the page
		wait_class = WebDriverWait(driver, 10)
		#this is the class for the umbrella of each individual review
		classes = wait_class.until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="search__results__list__item"]'))) 
		for class_ in classes:
			# Initialize an empty dictionary for each class
			class_dict = {}
			# Use try and except to skip the class elements that are empty. 
			# Use relative xpath to locate the title.
			try:
				title = class_.find_element_by_xpath('.//h6[@class="schedule-item__class__name"]').text
			except:
				title = 'none'

			# get the instructors name
			try:
				instructor = class_.find_element_by_xpath('.//div[@class="schedule-item__class__teacher"]').text
			except:
				instructor = 'none'
			#print('instructor = {}'.format(instructor))

			#get the rating of the class out of 5 
			try:
				rating = class_.find_element_by_xpath('.//span[@class="ratings__rating ratings--child"]/span').text
			except:
				rating = 'none'
			# print('rating = {}'.format(rating))

			#get the rtotal number of reviews
			try:
				reviews = class_.find_element_by_xpath('.//span[@class="ratings__count ratings--child"]').text
			except:
				reviews = 'none'
			# print('reviews = {}'.format(reviews))

			# get the time that the class starts 
			try:
				time = class_.find_element_by_xpath('.//div[@class="schedule-item__time"]/time').text
			except:
				time = 'none'
			# print('time = {}'.format(time))

			# find a way to use regex to take only the duration here otherwise we will return both the time and duration
			try:
				duration = class_.find_element_by_xpath('.//div[@class="schedule-item__time"]').text
			except:
				duration = 'none'
			# print('duration = {}'.format(duration))

			# get the venue of the class
			try:
				venue = class_.find_element_by_xpath('.//a[@class="schedule-item__venue__name"]').text
			except:
				venue = 'none'
			# print('venue = {}'.format(venue))

			# location of the venue
			try:
				location = class_.find_element_by_xpath('.//div[@class="schedule-item__venue__neighborhood"]').text
			except:
				location = 'none'
			# print('location = {}'.format(location))

			# get the tags linked to the class
			try:
				tags = class_.find_element_by_xpath('.//div[@class="schedule-item__venue__activities"]').text
			except:
				tags = 'none'
			# print('tags = {}'.format(tags))

			# get the price in credits of each class
			try:
				price = class_.find_element_by_xpath('.//a[@class="bt bt--sm bt--text-sm schedule-item__cta  _optimizely_search_test bt--primary bt--outline"]/span').text
			except:
				price = 'none'
			# print('price = {}'.format(price))

			
			class_dict['title'] = title
			class_dict['instructor'] = instructor	
			class_dict['rating'] = rating
			class_dict['reviews'] = reviews.replace('-','')
			class_dict['time'] = time	
			class_dict['duration'] = duration.split()[2]
			class_dict['venue'] = venue
			class_dict['location'] = location
			class_dict['tags'] = tags
			class_dict['price'] = price

			#writer.writerow(class_dict.keys())
			writer.writerow(class_dict.values())


		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//button[@class="disclosure-arrow disclosure-arrow--primary disclosure-arrow--next "]')))
		next_button.click()

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break

print("Data now listed in csv file")