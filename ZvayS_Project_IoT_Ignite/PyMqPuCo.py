#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os
import time
import ssl
import sys

class PuCo():
	def __init__(self):
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=30, cols=100))
		print ("""\x1b[1;34;48m
    ********************************************************************************		
    ********************   ____              ____     ______    ********************  
    ********************   |   |  |     |   /        |      |   ******************** 
    ********************   |___|  |     |  |         |      |   ******************** 
    ********************   |      |_____|   \____    |______|   ******************** 
    ********************                             	        ******************** 
    ********************************************************************************	
	""")
		print (" Welcome to \"PuCo\".")
		print ("\"PuCu\" is a library of \"ZvayS\"")
		print ("\"PuCu\" to get conf. \"IoT-Ignite\" with \"Mqtt\"\x1b[0m ")
		print ("\n"+"*"*75+"\n")


	#*************************************************************************************************************	
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
	def puco_Connect(self,host="mqtt.ardich.com",port=8883,keepalive=60):
		self.client.on_connect = self.__puco_on_connect
		self.client.on_message = self.__puco_on_message
		self.client.on_disconnect=self.__puco_on_disconnect
		self.client.connect(host, port, keepalive)
	#--------------------------------------------------------------------------------------------------
	#*************************************************************************************************************	

	#*************************************************************************************************************	
	def __puco_disconnect(self):
		print ("Disconnect PROCESS.")
		self.client.disconnect()
	#--------------------------------------------------------------------------------------------------
	def __puco_on_disconnect(self,client, userdata, rc):
		print("Disconnect OK")

	#--------------------------------------------------------------------------------------------------
	#*************************************************************************************************************
	#*************************************************************************************************************
	#*************************************************************************************************************
	


	#*************************************************************************************************************
	def publish_conf(self,node_id="pythonod",sensor_id="pysens"):

		self.client.publish(self.__topic_confGet().format(clnt_id=self.client_id,),
			payload=str(self.__confGet_message()),
			qos=2)

		self.client.loop_forever()

	#--------------------------------------------------------------------------------------------------
	def __topic_confGet(self):
		return "{clnt_id}/publish/ProductCatalog"

	#--------------------------------------------------------------------------------------------------
	#*************************************************************************************************************


	#*************************************************************************************************************
	def __puco_on_connect(self,client, userdata, flags, rc):
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

	#--------------------------------------------------------------------------------------------------
	def __puco_on_message(self,client, userdata, message):
		#print("Received message xxx '" + str(message.payload) + "' on topic '"
		#	+ message.topic + "' with QoS " + str(message.qos))
		print (str(message.payload))
		"""message_lib=json.loads(message.payload)
		try:
			getConf_operation=input("Please enter '1' to see the incoming data. Enter '0' if you want to terminate the process = ")
			if getConf_operation==1:
				print("Get Data : \n"+ str(message.payload))
				print("\n\nMessage Topic :"+message.topic )
				print("\n\nUse Qos : "+ str(message.qos))
				self.disconnect()
			else:
				self.disconnect()

			#print message_lib["header"]["msgId"]
			#print message_lib["header"]["maxMessageSize"]

			#print message_lib["body"][0]["params"][0]["hash"]
			#print message_lib["body"][0]["params"][0]["isComplete"]

			#print message_lib["body"][0]["params"][0]["products"][0]["services"]
			#print message_lib["body"][0]["params"][0]["products"][0]["contents"]
			#print message_lib["body"][0]["params"][0]["products"][0]["defaultApplication"]
			#print message_lib["body"][0]["params"][0]["products"][0]["hash"]
			#print message_lib["body"][0]["params"][0]["products"][0]["policyProfiles"][0]["mobileApnConfigs"]
			#print message_lib["body"][0]["params"][0]["products"][0]["policyProfiles"][0]["installationPolicies"]["trustedStores"]
			#. . .
		except KeyError:
			pass"""
			#--------------------------------------------------------------------------------------------------
	#*************************************************************************************************************


	#*************************************************************************************************************
	def __confGet_message(self):
		return """ 
			{
				"productId": "A6A67AE9-6AF5-4A0C-991A-16D0BC540D6A",
				"deviceProductHashValue": "0",
				"deviceConfInventory": {},
				"async": "false"
			}"""
		#--------------------------------------------------------------------------------------------------
	#*************************************************************************************************************
	#*************************************************************************************************************
	#*************************************************************************************************************

if __name__ == '__main__':
	classTest=PuCo()

	classTest.client_settings(client_id="python@deneme")
	classTest.usr_psw_set(user_name="python123",password="12345678")
	classTest.puco_Connect()

	classTest.publish_conf(node_id="pythonod",sensor_id="pysens")	
		
		