# -*- coding: utf-8 -*-
"""
@author: xin
@python3.7.2
@ 参考 https://github.com/Jack-Cherish/python-spider
"""
from splinter.browser import Browser
from time import sleep
import configparser

class Residence(object):
	driver_name = ''
	"""网址"""
	login_url = "http://203.86.55.48/Residence"
	initmy_url = "http://203.86.55.48/Residence/a?login"
	refresh_count = 1

	def __init__(self):
		# http://chromedriver.storage.googleapis.com/index.html?path=2.20/
		# chromedriver.exe 放置在 python.exe 所在路径
		self.driver_name = 'chrome'

	def login(self, username, passwd):
		self.browser.visit(self.login_url)
		self.browser.fill("username", username)
		# sleep(1)
		self.browser.fill("password", passwd)
		print(u"等待验证码，自行输入...")
		while True:
			if self.browser.url != self.initmy_url:
				sleep(1)
			else:
				break

	def permit(self, permitname, idcard):
		if self.browser.find_by_id('mainFrame'):
			with self.browser.get_iframe('mainFrame') as frame:
				# 初次申请（新办）
				frame.find_by_xpath('//select[@id="type"]/option')[1].click()
				if frame.find_by_text(u"可预约"):
					frame.find_by_text(u"可预约").click()
					# 业务预约
					frame.fill("0_0", permitname)
					frame.fill("idcard_0_0", idcard)
					# 确认预约
					frame.find_by_id("btnSave").click()
					return True
				else:
					sleep(1)
					print(u"刷新页面 %d..." % self.refresh_count)
					frame.execute_script("window.location.href = \"/Residence/a/rrs/reservation/form\";")
					self.refresh_count += 1
					return False

	def start(self, username, passwd, permitname, idcard):
		self.browser = Browser(driver_name=self.driver_name)
		self.browser.driver.set_window_size(1400, 1000)
		# 登录
		self.login(username, passwd)
		# 点击 '业务预约'
		# self.browser.click_link_by_href("/Residence/a/rrs/agreement")
		print(u"我认真阅读并接受以上协议...")
		if self.browser.find_by_id('mainFrame'):
			with self.browser.get_iframe('mainFrame') as frame:
				# frame.find_by_id('cb').click()
				# frame.find_by_id('tj').click()
				frame.execute_script("window.location.href = \"/Residence/a/rrs/reservation/form\";")
		print(u"预约申请...")
		while True:
			if self.permit(permitname, idcard):
				break


if __name__ == '__main__':
	cf = configparser.ConfigParser()
	# residence.ini 编码格式：utf-8 （无BOM）
	cf.read("residence.ini", encoding='utf-8')
	# 用户名，密码
	username = cf.get(u"Config", "username")
	passwd = cf.get("Config", "password")
	# 申请人姓名，身份证号
	permitname = cf.get("Config", "proposer")
	idcard = cf.get("Config", "idcard")
	residence = Residence()
	residence.start(username, passwd, permitname, idcard)
