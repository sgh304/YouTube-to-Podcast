import selenium.webdriver.common.keys
import selenium.common.exceptions
import selenium.webdriver
import time

class NoWebdriverException(Exception):
	pass

class TimeoutException(Exception):
	pass

class PatientDriver():
	'''A simple webdriver that automatically waits for elements to load before executing actions. For when the running time is not so important, but the data is'''
	def __init__(self, executable_path = 'webdriver/chromedriver/chromedriver.exe', timeout = 5):
		# User options
		self.executable_path = executable_path
		self.timeout = timeout

		# Chrome options
		self.chrome_options = selenium.webdriver.ChromeOptions()
		self.chrome_options.add_experimental_option('detach', True)
		self.chrome_options.add_argument('--disable-extensions')
		self.chrome_options.add_argument('--log-level=3')
		self.chrome_options.add_argument('--start-maximized')

		# State variables
		self.webdriver = None

	# GENERAL DRIVING
	def open(self):
		'''Opens the browser window'''
		self.webdriver = selenium.webdriver.Chrome(executable_path = self.executable_path, chrome_options = self.chrome_options)

	def close(self):
		self.check_for_webdriver()
		self.webdriver.close()

	def check_for_webdriver(self):
		'''Checks if the browser window is open'''
		if not self.webdriver:
			raise NoWebdriverException

	def go_to(self, url):
		'''Navigates to a webpage'''
		self.check_for_webdriver()
		last_page = self.webdriver.find_element_by_tag_name('html')
		self.webdriver.get(url)
		while True:
			self.current_page = self.webdriver.find_element_by_tag_name('html')
			if last_page.id != self.current_page.id:
				return
			time.sleep(1)

	def wait_for_element(self, xpath, timeout = None):
		'''Waits for an element matching the xpath to load on a webpage'''
		return self.wait_for_elements(xpath, n = 1, timeout = timeout)[0]

	def wait_for_elements(self, xpath, n = 1, timeout = None):
		'''Waits for at least n elements matching the xpath to load on a webpage'''
		self.check_for_webdriver()
		waited = 0
		while True:
			if (timeout and waited > timeout) or (self.timeout and waited > self.timeout):
				raise TimeoutException
			elements = self.webdriver.find_elements_by_xpath(xpath)
			if len(elements) >= n:
				return elements
			else:
				time.sleep(1)
				waited += 1

	def clear(self, xpath):
		'''Clears an element on a webpage'''
		self.check_for_webdriver()
		self.wait_for_element(xpath).clear()

	def click(self, xpath):
		'''Clicks on an element on a webpage'''
		self.check_for_webdriver()
		self.wait_for_element(xpath).click()

	def send_keys(self, xpath, keys):
		'''Sends keys to an element on a webpage'''
		self.check_for_webdriver()
		self.wait_for_element(xpath).send_keys(keys)