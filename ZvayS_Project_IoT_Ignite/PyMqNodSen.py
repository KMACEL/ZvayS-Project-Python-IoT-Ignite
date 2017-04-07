#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os
import time
import ssl
import sys


class NodSen():
	def __init__(self):
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=30, cols=100))
		print ("""\x1b[1;34;48m
    *******************************************************************************		
    ***********            _____    ___      _____     _____           ***********
    ***********   |\   |  |     |  |   \    /     \   |       |\   |   ***********
    ***********   | \  |  |     |  |    \   |____     |____   | \  |   ***********
    ***********   |  \ |  |     |  |    /        \    |       |  \ |   ***********
    ***********   |   \|  |_____|  |___/   \______|   |_____  |   \|   ***********
    ***********                                                        ***********       
    *******************************************************************************	
	""")
		print (" Welcome to \"NodSen\".")
		print ("\"NodSen\" is a library of \"ZvayS\"")
		print ("\"NodSen\" to transfer \"Node\" and \"Sensor\" invertory \"IoT-Ignite\" with \"Mqtt\"\x1b[0m ")
		print ("\n"+"*"*75+"\n")

#*************************************************************************************************************	
	def client_settings(self,client_id, protocol=mqtt.MQTTv311): 
		self.client_id=client_id
		self.client=mqtt.Client(client_id,protocol)
		self.certs_set()
	#--------------------------------------------------------------------------------------------------
	
	def certs_set(self,path=os.getcwd(),ser_name="/GlobalSign_Root_CA.pem",tls_version=ssl.PROTOCOL_TLSv1):
		self.client.tls_set(path+ser_name, tls_version=tls_version)
		#client.tls_insecure_set(True)
	
	#--------------------------------------------------------------------------------------------------
	def usr_psw_set(self,user_name,password): 
		self.client.username_pw_set(user_name,password)

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************


#*************************************************************************************************************	
	def nodsen_Connect(self,host="mqtt.ardich.com",port=8883,keepalive=60):
		self.client.on_message = self.__nodsen_on_message
		self.client.on_connect = self.__nodsen_on_connect
		self.client.on_disconnect=self.___nodsen_on_disconnect
		self.client.connect(host, port, keepalive)

		self.client.loop_start()
		#time.sleep(1)

	#--------------------------------------------------------------------------------------------------
	def nodsen_disconnect(self):
		self.client.loop_stop()

		print ("Disconnect PROCESS.")
		self.client.disconnect()

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************

#*************************************************************************************************************
	def publish_nodSen(self,nodSenPath):

		self.client.publish(
			topic=self.__topic_nodeSenSend().format(
					clnt_id=self.client_id),
			payload=str(self.__nodeSenSend_message(nodSenPath)),
			qos=2)

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************


#*************************************************************************************************************
	def __nodeSenSend_message(self,nodSenPath):
		path=os.getcwd()
		self.code=open(path+"/"+nodSenPath)   #*****************
		self.code=self.code.read()

		return self.code
	#--------------------------------------------------------------------------------------------------

#*************************************************************************************************************


#*************************************************************************************************************
	def __topic_nodeSenSend(self):
		return "{clnt_id}/publish/DeviceProfile/Status/DeviceNodeInventory"
	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************


#*************************************************************************************************************
	def __nodsen_on_connect(self,client, userdata, flags, rc):
		global loop_flag
		if (rc==0):
			print("Connection successful") 
		elif (rc==1):
			print("Connection Failed - Incorrect Protocol Version !")
		elif (rc==2):
			print("Connection Failed - Invalid Client Identifier !")
		elif (rc==3):
			print("Connection Failed - Server Unavailable !")
		elif (rc==4):
			print("Connection Failed - Bad Username or Password !")
		elif (rc==5):
			print("Connection Failed - Not Authorised !")
		time.sleep(1) #*************


	#--------------------------------------------------------------------------------------------------
	def __nodsen_on_message(self,client, userdata, message):
		self.m_topic=message.topic
		message=str(message.payload).split(":")
		if (message[1][:2]=="tr"):
			print ("Your message has been successfully delivered ...")
			#print ("Message : " ,str(self.code))
			print ("Publish Topic :",str(self.m_topic))
			print("\n")
			#time.sleep(0.2)#****************************
			
		"""	
		
		else:
			print ("Error! Your message has not been forwarded !")
			print ("Try Again!")"""
			
		

	#--------------------------------------------------------------------------------------------------
	def ___nodsen_on_disconnect(self,client, userdata, rc):
		print("Disconnect OK")

	#--------------------------------------------------------------------------------------------------

	def __on_publish(self,mosq, obj, mid):
		print("mid: " + str(mid))

	#--------------------------------------------------------------------------------------------------

	def __on_long(self):
		pass

	#--------------------------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------------------------

	def message_retry(self):
		pass

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************


#*************************************************************************************************************
#************************************************ NodSen End ***************************************************
#*************************************************************************************************************



if __name__ == '__main__':
	classTest=NodSen()

	classTest.client_settings(client_id="python@deneme")
	classTest.usr_psw_set(user_name="python123",password="12345678")
	classTest.nodsen_Connect()


	classTest.publish_nodSen(nodSenPath="nodSenList.txt")
	time.sleep(2)
	

	classTest.nodsen_disconnect()
