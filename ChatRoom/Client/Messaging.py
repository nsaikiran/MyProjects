#Encoding part

#(c) ChatRoom Team (team-09 SG-06 Batch 2010)
import base64

def Encode(data):
	return base64.b64encode(data)
def Decode(data):
	return base64.b64decode(data)

"""

0 - conn [0 ,0- fail ,1 - success ,2- disconnect]	THis is only for client
1 - register [0-fail , 1- success]	[1,[name,uname,passwd]]
2 - log in [ 0- fail ,1 -success ]	[2,[uname,passwd]]
3 - sms [sender , sms][3,sender,sms]	[3,sms] based on conn we determine uname
4 - update [] [4,1,[username,ip]] or [4,0,username]
5-
"""
Tags=["[Connection]","[Registration]","[Log In]","[Message]","[UPDATE]","[Log Out]"]
Codes={0:["FAILED","ACCEPTED","YOU ARE DISCONNECTED / SERVER SHUT DOWN"],1:["FAILED","SUCCESSFUL"],2:["FAILED","SUCCESSFUL"],4:["LOGGED IN","LOGGED OUT"]}

#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
