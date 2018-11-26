#!/usr/bin/python


import httplib2
import httplib
import socket
import exceptions
import urllib2
from bs4 import BeautifulSoup
import json
import io
import ConfigParser
import re

# Load the configuration file
with open("config.ini") as f:
	sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

class host:
		name = ''
		ip = ''
		status ="n"
		temp = "0"
		hum = "0"
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
		channelpress = "0"
		channelwidp = "0"

class server():
	address = config.get('Serv','ip')
	port = config.get('Serv','port')



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
			self.hum = self.sdata[0].partition(': ')           #Position 0 on the list represents humidity with value  we are saveing it to var for partition
			print self.hum[2]			#Diagnostic echo representing humidity value
			self.temp = self.sdata[1].partition(': ')		#same as above
			print self.temp[2]
		except(urllib2.URLError):
			host.status="Down"

class weatherc():

	def __init__(self,):
		self.conn = json.loads(urllib2.urlopen("http://" + server.address + ":" + server.port + "/API/chanellist?format=json").read())
		#print (self.conn['results'][1]['city'])
		for con in self.conn['results']:
			host.web = con['web']
			print(host.web)
			host.country = con['country']
			host.city = con['city']
			host.cityg = con['cityg']
			h = httpck(host.web)
			#print host.status
			self.page = urllib2.urlopen("http://"+host.web+"/"+host.country+"/"+host.city+"_"+host.cityg+"/") #Getting target site
			self.soup = BeautifulSoup(self.page, features="html.parser") #Scrapeing downloaded page
			self.findm = self.soup.find('tr', attrs={'class':'k2'})
			self.date = self.findm.find('td', attrs={'height':'64', 'width':'156'}).text.strip()
			print (host.city)
			print self.date
			host.polingdate = self.date
			self.weather = self.findm.find('div', attrs={'id':'ico_now_under'}).text.strip()
			print self.weather
			host.weater = self.weather
			self.channeltr = self.findm.find_all('td')
			self.channelr = re.findall(r'[-\d]+', self.channeltr[2].text.strip())[0]#find all digits to find temperature and delete the html tags
			host.channeltempn = self.channelr
			print (self.channelr+ " C")
			self.windt = self.channeltr[3].text.strip().partition(' ')#strip and partition data to get wind temperature
			print (self.windt[0]+ " m/s")
			self.fdtr = self.soup.find('div', attrs={'class': 'czas now'}).text.strip()#find predicted hour equal to OSMO model
			print self.fdtr
			self.ftempt = self.soup.find('div', attrs={'class': 'autodin'})
			host.channeltempf = re.findall(r'[-\d]+', self.ftempt.text.strip())[0] #Find digit then select itme 0 from the list and delete html tags
			print (host.channeltempf+" C")
			self.press = self.soup.find_all('div', attrs={'class':'autodin'})
			host.channelpress = re.findall(r'[-\d]+', self.press[2].text.strip())[0] #Find all digits then select item number 2 from the list and delete html tags then print
			print (host.channelpress+ " hPa")
			host.channelwidp = re.findall(r'[-\d]+', self.press[3].text.strip())[0]
			print (host.channelwidp + " m/s")

weatherc()


class runapp():
	def __init__(self,):
		#try:
		self.conect = json.loads(urllib2.urlopen("http://" + server.address + ":" + server.port + "/API/devlist?format=json").read())
		# print (conect['results'][0][''])
		for con in self.conect['results']:
			host.name = con['name']
			host.ip = con['ip']
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

