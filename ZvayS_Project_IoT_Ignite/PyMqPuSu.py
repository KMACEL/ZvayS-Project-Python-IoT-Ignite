#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paho.mqtt.client as mqtt  
import os
import time
import ssl
import sys


#********************   ____             ------  
#********************   |   |  |     |  |         |     |   ********************
#********************   |   |  |     |  |------   |     |   ********************
#********************   |---   |     |        |   |     |   ********************
#********************   |	   |_____|  ------|   |_____|   ********************
class PuSu():
	def __init__(self):
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=30, cols=100))
		print ("""\x1b[1;34;48m
    ********************************************************************************		
    ********************   ____             ______              ********************
    ********************   |   |  |     |  /      \   |     |   ********************
    ********************   |___|  |     |  |_____     |     |   ********************
    ********************   |      |     |        \    |     |   ********************
    ********************   |      |_____|  \______|   |_____|   ********************
    ********************                                        ********************		
    ********************************************************************************	
	""")
		print (" Welcome to \"PuSu\".")
		print ("\"PuSu\" is a library of \"ZvayS\"")
		print ("\"PuSu\" to transfer data \"IoT-Ignite\" with \"Mqtt\"\x1b[0m ")
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
	def pusu_Connect(self,host="mqtt.ardich.com",port=8883,keepalive=60):
		self.client.on_message = self.__pusu_on_message
		self.client.on_connect = self.__pusu_on_connect
		self.client.on_disconnect=self.__pusu_on_disconnect
		self.client.connect(host, port, keepalive)

		self.client.loop_start()
		#time.sleep(1)

	#--------------------------------------------------------------------------------------------------
	def pusu_disconnect(self):
		self.client.loop_stop()

		self.client.publish(topic=
			self.__topic_sensorNodeStatue().format(
					clnt_id=self.client_id),
			payload=str(self.__sensorStatue_message(self.node_id,self.sensor_id,0)))

		self.client.publish(topic=
			self.__topic_sensorNodeStatue().format(
					clnt_id=self.client_id),
			payload=str(self.__nodeStatue_message(self.node_id,0)))


		print ("Disconnect PROCESS.")
		self.client.disconnect()

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************
	
	
#*************************************************************************************************************
	def publish_data(self,node_id,sensor_id,value):
		self.node_id=node_id
		self.sensor_id=sensor_id

		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		self.client.publish(topic=
			self.__topic_sensorNodeStatue().format(
					clnt_id=self.client_id),
			payload=str(self.__sensorStatue_message(node_id,sensor_id,1)))

		self.client.publish(topic=
			self.__topic_sensorNodeStatue().format(
					clnt_id=self.client_id),
			payload=str(self.__nodeStatue_message(node_id,1)))
		#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

		self.client.publish(
			topic=self.__topic_dataSend().format(
					clnt_id=self.client_id,
					node_id=self.node_id,
					sensor_id=self.sensor_id),
			payload=str(self.__dataSend_message(value)),
			qos=2)

	#--------------------------------------------------------------------------------------------------
#*************************************************************************************************************


#*************************************************************************************************************
	def __dataSend_message(self,value):
		self.value=value
		return """
			{
				data:
				{
					sensorData:
					[
						{
							date: %s,
							values:[%s]
						}
					],
				formatVersion:2
			}
		}""" %(str(time.time())[:10]+"000",value)
	#--------------------------------------------------------------------------------------------------

	def __sensorStatue_message(self,nd_id,sns_id,stat):
		return """
		{
  			"data":
  			[
    			{
      				"nodeId":"%s" ,
      				"thingId": "%s",
      				"connected":%i,
      				"descrtiption": "Pusu",
    			}
  			]
		}"""%(nd_id,sns_id,stat)
		#--------------------------------------------------------------------------------------------------

	def __nodeStatue_message(self,nd_id,stat):
		return """
		{
  			"data":
  			[
    			{
      				"nodeId":"%s" ,
      				"connected":%i,
      				"descrtiption": "Pusu",
    			}
  			]
		}""" %(nd_id,stat)
#*************************************************************************************************************


#*************************************************************************************************************
	def __topic_dataSend(self):
		return "{clnt_id}/publish/DeviceProfile/{node_id}/{sensor_id}"
	#--------------------------------------------------------------------------------------------------

	def __topic_sensorNodeStatue(self):
		return "{clnt_id}/publish/DeviceProfile/Status/DeviceNodePresence"
#*************************************************************************************************************


#*************************************************************************************************************
	def __pusu_on_connect(self,client, userdata, flags, rc):
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
	def __pusu_on_message(self,client, userdata, message):
		self.m_topic=message.topic
		message=str(message.payload).split(":")
		if (message[1][:2]=="tr"):
			print ("Your message has been successfully delivered ...")
			print ("Message : " ,str(self.value))
			print ("Publish Topic :",str(self.m_topic))
			print("\n")
			#time.sleep(0.2)#****************************
			
			
		
		else:
			print ("Error! Your message has not been forwarded !")
			print ("Try Again!")
			
		

	#--------------------------------------------------------------------------------------------------
	def __pusu_on_disconnect(self,client, userdata, rc):
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
	def __node_sensor_online(self,node_id,sensor_id):
		pass
#*************************************************************************************************************
#************************************************ PuSu End ***************************************************
#*************************************************************************************************************


if __name__ == '__main__':
	classTest=PuSu()

	classTest.client_settings(client_id="python@deneme")
	classTest.usr_psw_set(user_name="python123",password="12345678")
	classTest.pusu_Connect()

	classTest.publish_data(node_id="pythonod",sensor_id="pysens",value=70)	
	time.sleep(2)
	

	classTest.pusu_disconnect()
	

	