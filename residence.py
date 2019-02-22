# -*- coding: utf-8 -*-
"""
@author: xin
@ python3
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
	order_url = "http://203.86.55.48/Residence/a/rrs/reservation/form"
	order_script = "window.location.href = \"/Residence/a/rrs/reservation/form\";"
	reserve_url = "http://203.86.55.48/Residence/a/rrs/reservation/reserveInfo"
	refresh_count = 1

	def __init__(self):
		# http://chromedriver.storage.googleapis.com/index.html?path=2.20/
		# 下载的 chromedriver.exe 需要和安装的chrome版本匹配
		# chromedriver.exe 放置在 python.exe 所在路径，
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

	def permit(self, proposer, idcard):
		if self.browser.find_by_id('mainFrame'):
			with self.browser.get_iframe('mainFrame') as frame:
				try:
					# 初次申请（新办）
					frame.find_by_xpath('//select[@id="type"]/option')[1].click()
					wait_count = 1
					while frame.url == self.order_url:
						print(u"查询状态 %d" % wait_count)
						wait_count += 1
						if frame.find_by_text(u"已约满"):
							break
					if frame.find_by_text(u"可预约"):
						wait_count = 1
						frame.find_by_text(u"可预约").click()
						while True:
							print(u"等待预约页面加载 %d " % wait_count)
							wait_count += 1
							if frame.find_by_id(u"idcard_0_0"):
								break
						# 业务预约
						frame.fill("0_0", proposer)
						frame.fill("idcard_0_0", idcard)
						# 确认预约
						frame.find_by_id("btnSave").click()
						print(u"请确认预约结果")
						return True
					else:
						print(u"刷新页面 %d..." % self.refresh_count)
						if wait_count < 3:
							sleep(1)						
						# frame.execute_script(self.order_script)
						frame.execute_script("gradeChange();")
						self.refresh_count += 1
						return False
				except Exception as e:
					print(e)
					print(u"刷新失败...")
					frame.execute_script(self.order_script)
					return False

	def start(self, username, passwd, proposer, idcard):
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
				frame.execute_script(self.order_script)
		print(u"预约申请...")
		while True:
			if self.permit(proposer, idcard):
				break


if __name__ == '__main__':
	cf = configparser.ConfigParser()
	# residence.ini 编码格式：utf-8 （无BOM）
	cf.read("residence.ini", encoding='utf-8')
	# 用户名，密码
	username = cf.get(u"Config", "username")
	passwd = cf.get("Config", "password")
	# 申请人姓名，身份证号
	proposer = cf.get("Config", "proposer")
	idcard = cf.get("Config", "idcard")
	residence = Residence()
	residence.start(username, passwd, proposer, idcard)
