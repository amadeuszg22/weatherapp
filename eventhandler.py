#!/usr/bin/python


import httplib2
import httplib
import socket
import exceptions
import urllib2
from bs4 import BeautifulSoup
import sys
import io
import ConfigParser
import re

# Load the configuration file
with open("config.ini") as f:
	sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

class host:
		name= config.get('Host1', 'name')
		ip= config.get('Host1', 'ip')
		status="n"
		temp ="0"
		hum ="0"
	#Weather  channel data
		web = "urls"
		country = "pl"
		city ="waw"
		cityg ="Waw"
		polingdate = "Date"
		weater = "zachm"
		channeltempn = "0"
		channelwindn = "0"
		channeltempf = "0"

class httpck():
	def __init__(self,ip):
		try:
			self.ip = ip
			con = httplib.HTTPConnection(ip)
			con.request("GET", "/")
			self.res = con.getresponse()
			if self.res.status == 200:
				host.status="UP"
				#print host.status
			else:
				host.status="Down"
		except(httplib.HTTPException, RuntimeError, TypeError, NameError, socket.error,
					socket.gaierror):
			host.status="Down"
			print host.status

class pagepars():
	def __init__(self, ip):
		try:
			self.ip = ip

			self.page = urllib2.urlopen("http://"+ip+"/") #Getting target site 
			self.soup = BeautifulSoup(self.page, features="html5lib") #Scrapeing downloaded page
			self.findm = self.soup.find('title')	 #Parsing site to find desired paragrpah  that contains desired data
			self.msg = self.findm.text.strip()	  #Stirping data to get message
			self.finddesc = self.soup.find('h3')	#Parsing site to find desired paragrpah  that contains desired data
			self.desc = self.finddesc.text.strip()   #Stirping data to get description
			self.finddata = self.soup.find('pre')   #Parsing site to find desired paragrpah  that contains desired data
			self.data = self.finddata.text.strip() #Stirping data to get temperature and humidity Data
			self.sdata = self.data.splitlines()   #Data variable comes as multiline string, command convers multiline string to the list 
			self.humraw = self.sdata[0]           #Position 0 on the list represents humidity with value  we are saveing it to var for partition
			self.hum = self.humraw.partition(': ') #Variable partition to get onlty humidtity value  without description
			#print hum[2]			#Diagnostic echo representing humidity value
			self.tempraw = self.sdata[1]		#same as above
			self.temp = self.tempraw.partition(': ')
			#print temp[2]
		except(urllib2.URLError):
			host.status="Down"

class weatherc():

	def __init__(self,):
		for section_name in config.sections():
								#print 'Section:', section_name
								match = re.match(r"^Weather*", section_name)
								if match:
										#for name, value in config.items(section_name):
										host.web = config.get(section_name, 'web')
										host.country = config.get(section_name, 'country')
										host.city = config.get(section_name, 'city')
										host.cityg = config.get(section_name, 'cityg')
										h = httpck(host.web)
										#print host.status
										self.page = urllib2.urlopen("http://"+host.web+"/"+host.country+"/"+host.city+"_"+host.cityg+"/") #Getting target site
										self.soup = BeautifulSoup(self.page, features="html.parser") #Scrapeing downloaded page
										self.findm = self.soup.find('tr', attrs={'class':'k2'})
										self.dateraw = self.findm.find('td', attrs={'height':'64', 'width':'156'})
										self.date = self.dateraw.text.strip()
										print self.date
										host.polingdate = self.date
										self.weatherraw = self.findm.find('div', attrs={'id':'ico_now_under'})
										self.weather = self.weatherraw.text.strip()
										print self.weather
										host.weater = self.weather
										self.channeltr = self.findm.find_all('td')
										self.channelr = self.channeltr[2]
										self.channelra = self.channelr.text.strip()
										self.channelraw = re.findall(r'[-\d]+', self.channelra)
										host.channeltempn = self.channelraw[0]
										print (self.channelraw[0]+ " C")
										self.windt = self.channeltr[3]
										self.windte = self.windt.text.strip()
										self.windtem = self.windte.partition(' ')
										print (self.windtem[0]+ " m/s")
										self.fdtr = self.soup.find('div', attrs={'class': 'czas now'})
										self.ftd = self.fdtr.text.strip()
										print self.ftd
										self.ftempt = self.soup.find('div', attrs={'class': 'autodin'})
										self.ftempte  = self.ftempt.text.strip()
										self.ftemp = re.findall(r'[-\d]+', self.ftempte)
										host.channeltempf = self.ftemp[0]
										print (host.channeltempf+" C")
										self.press = self.soup.find_all('div', attrs={'class':'autodin'})
										print re.findall(r'[-\d]+', self.press[2].text.strip())[0]


weatherc()


class runapp():
	def __init__(self,):
		#try:
			for section_name in config.sections():
					#print 'Section:', section_name
				match = re.match(r"^Host*", section_name)
				if match:
						#for name, value in config.items(section_name):
						host.name = config.get(section_name, 'name')
						host.ip = config.get(section_name, 'ip')
						h = httpck(host.ip)
						try:
							cpagepars = pagepars(host.ip)
							host.temp  = cpagepars.temp[2]
							host.hum = cpagepars.hum[2]
						except(AttributeError):
							print "Host Down"

						print host.name + ":" + host.ip + " " + "Host Status:" + host.status

						try:
							print("Host HTTP Service status:")
							print h.res.status, h.res.reason
							print "ESP Message:"
							print cpagepars.msg
							print cpagepars.desc
							print cpagepars.data
						except(AttributeError):
							print "Host Down"



runapp()

