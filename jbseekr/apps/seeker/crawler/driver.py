import time

#from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import (Select, WebDriverWait)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django.conf import settings



class Driver:
	def __init__(self, path=None):
		self.driver = None
		self.path = path if path else settings.CHROMEDRIVER_PATH
		self.scrolls = 0
		self.scrolls_number = 0
		self.scroll_start_height = 0
		self.client_height = None

	def open(self, headless=True, no_sandbox=True):
		chrome_options = webdriver.ChromeOptions()
		# No images
		prefs = {"profile.managed_default_content_settings.images": 2}
		chrome_options.add_experimental_option("prefs", prefs)

		time.sleep(1)

		if no_sandbox:
			chrome_options.add_argument('--no-sandbox')

		if headless:
			chrome_options.add_argument('--headless')

		"""
		ua = UserAgent()
		userAgent = ua.random
		chrome_options.add_argument(f'user-agent={userAgent}')
		"""

		chrome_options.add_argument("--incognito")
		self.driver = webdriver.Chrome(self.path, chrome_options=chrome_options)
		self.driver.set_window_position(0, 0)
		self.driver.maximize_window()

	def close(self):
		self.driver.close()

	def get_by_xpath(self, xpath):
		return self.driver.find_element_by_xpath(xpath)

	def get_by_css(self, css):
		return self.driver.find_element_by_css_selector(css)

	def get_by_id(self, id):
		return self.driver.find_element_by_id(id)

	def get_by_text(self, text):
		return self.driver.find_element_by_xpath(f"//*[contains(text(), '{text}')]")

	def get_by_class(self, class_name):
		return self.driver.find_element_by_class_name(class_name)

	def get_elements_by_class(self, class_name):
		return self.driver.find_elements_by_class_name(class_name)

	def get_url(self, url):
		return self.driver.get(url)

	def get_select_by_xpath_and_value(self, xpath, value):
		select = Select(self.driver.find_element_by_xpath(xpath))
		select.select_by_value(str(value))

	def get_class_name_attribute(self, name, attribute):
		return self.driver.find_element_by_class_name(name).get_attribute(attribute)

	@staticmethod
	def get_inner_elements_by_tag(container, tag):
		return container.find_elements_by_tag_name(tag)

	@staticmethod
	def get_inner_elements_by_class(container, name):
		return container.find_elements_by_class_name(name)

	@staticmethod
	def get_inner_elements_by_id(container, id):
		return container.find_elements_by_id(id)

	@staticmethod
	def get_inner_elements_by_text(container, text):
		return container.find_elements_by_xpath(f"//*[contains(text(), '{text}')]")

	def get_elements_by_tag(self, tag):
		return self.driver.find_elements_by_tag_name(tag)

	def get_elements_by_id(self, id):
		return self.driver.find_elements_by_id(id)

	def get_elements_by_text(self, text):
		return self.driver.find_elements_by_xpath(f"//*[contains(text(), '{text}')]")

	def wait_until_title_contains_keyword(self, title):
		try:
			WebDriverWait(self.driver, 5).until(EC.title_contains(title))
		except Exception:
			pass

	def wait_until_element_is_loaded_by_xpath(self, xpath, seconds):
		try:
			WebDriverWait(self.driver, seconds).until(EC.element_to_be_clickable((By.XPATH, xpath)))
		except Exception:
			pass

	def wait_until_element_is_loaded_by_class(self, class_name, seconds):
		try:
			WebDriverWait(self.driver, seconds).until(EC.element_to_be_clickable((By.CLASS, class_name)))
		except Exception:
			pass

	def wait_until_element_is_loaded_by_id(self, id, seconds):
		try:
			WebDriverWait(self.driver, seconds).until(EC.element_to_be_clickable((By.ID, id)))
		except Exception:
			pass

	def scroll_bottom(self):
		script = "window.scrollTo(0,document.body.scrollHeight);"
		self.driver.execute_script(script)

	def scroll_down(self):
		if not self.client_height:
			self.client_height = self.get_client_height()

		script = f"window.scrollTo({self.scroll_start_height},{self.scroll_start_height+self.client_height});"
		self.driver.execute_script(script)
		self.scrolls_number += 1

	def get_client_height(self):
		return self.driver.execute_script("return document.body.clientHeight")

	def open_in_new_tab(self, url):
		self.driver.execute_script(f"window.open('{url}','_blank');")

	def select_dropdown_option(self, text):
		select = Select(self.get_by_xpath(xpath="//*[@id='of_provincia_chosen']"))
		select.select_by_visible_text(text)

	def wait_implicit_time(self, seconds):
		self.driver.implicitly_wait(seconds)
