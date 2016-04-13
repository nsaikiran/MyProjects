#Main program for server.
#DO NOT EDIT
##(c) ChatRoom Team (team-09 SG-06 Batch 2010)

import ChatRoomServerGui as Gui
import socket
import gtk
import Dialog
import gobject
import Messaging as code
from DataBase import DB
PchatGUI=Dialog.Dialog_PrivateChat

class Dialog_ShowUser(Dialog.DialogBox):
	def __init__(self,parent):
		Dialog.DialogBox.__init__(self,"About",parent)
		self.label=gtk.Label("Name:")
		self.dialog.vbox.pack_start(self.label,False,False,0)
	def Run(self,uname,name):
		self.label.set_text("Username : %s \nName : %s"%(uname,name))
		self.dialog.show_all()
		res=self.dialog.run()
		self.dialog.hide()

#Main Class ...
class Server(Gui.ServerGUI):
	def __init__(self):
		Gui.ServerGUI.__init__(self)
		self.obj_editport=Dialog.Dialog_EditPort(self)
		self.obj_usrdetails=Dialog_ShowUser(self)
		self.RESET()
		self.server=0	#not running
		self.listen=0	#not accepting connection
		self.NewUserListView.connect('row-activated',self.DisplayUserDetails)#double click to activate .
		self.UserListView.connect('row-activated',self.PrivateChat)	#shows online users , double click to private chat
		self.b_start_srvr.connect('clicked',self.StartServer)
		self.b_stop_srvr.connect('clicked',self.StopServer)
		#variable ...
		
		self.connection_list={}	#all connections
		self.myname='admin'
		self.userlist={}	#{username:ip}
		self.connected_pchat={}
		
		self.userlist[code.Encode('admin')]=code.Encode(self.ip)
		
		self.b_editport.connect("clicked",self.EditPort)
		self.b_close_srvr.connect('clicked',self.CloseServer)
		self.b_send.connect('clicked',self.SendMessage)
		self.send_sms.connect('activate',self.SendMessage)
		self.b_clear.connect('clicked',self.ClearField)
		self.b_clearview.connect('clicked',self.ClearView)
		self.connect('destroy',self.CloseServer)
		#self.StartServer()
		#pass

	def StartServer(self,widget):
		if not self.server:
			self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			self.sock.bind((self.ip,self.port))
			self.sock.listen(5)
			self.server_id=gobject.io_add_watch(self.sock,gobject.IO_IN,self.accept_connection)
			self.b_editport.hide()
			self.server=1
		self.listen=1
		widget.hide()
		self.l_srvr_status.set_text('Listening for clients . .')
		self.b_stop_srvr.show()
		return True

	def StopServer(self,widget):
		widget.hide()
		self.b_start_srvr.show()
		self.l_srvr_status.set_text('Stopped listening . .')
		self.listen=0
		return True

	def accept_connection(self,source,condition):	#source = self.socket , codition = IO_IN
		conn,addr=self.sock.accept()
		if self.listen:
			_id=gobject.io_add_watch(conn,gobject.IO_IN,self.GotMessage)
			self.connection_list[conn]=[addr[0],None,_id]	#add,uname,(_id -> id of conn )
			conn.sendall("[0,1]|")# connection accepted ...
			conn.sendall("[4,2,"+str(self.userlist)+"]|")	#sending userlist .
			self.PrintText('[Note] :Accepted '+addr[0])
		else:
			self.PrintText('[Note] :Rejected '+addr[0])
			conn.sendall("[0,0]|")# connection rejected . .
		return True

	def CloseServer(self,widget):
		DB.CloseDB()
		if self.server:
			gobject.source_remove(self.server_id)
			for conn in self.connection_list:
				pass
		self.CloseWindow(self)

	def RESET(self):
		self.ip=findip()
		self.l_srvr.set_text(self.ip+':'+str(self.port))
		self.b_stop_srvr.hide()
		#self.b_close_srvr.hide()
		self.UpDateUserList()

	def DisplayUserDetails(self, treeview, path, column):
		iter=self.newusermodel.get_iter(path)
		uname=self.newusermodel.get_value(iter,0)
		name=DB.Name(uname)
		self.obj_usrdetails.Run(uname,name[0][0])
		return True

	def UpDateUserList(self):
		self.newusermodel.clear()
		for tup in DB.GetAll():
			self.newusermodel.append([tup[0]])

	def Send2All(self,text,dont=None):	#we don't want to send sms to its sender
		print dont
		if dont!=None:
			for conn in self.connection_list:
				x=self.connection_list[conn]
				if x[1]!=None and dont!=x[1]:
					print "send to ",self.connection_list[conn][1]
					conn.send(text+'|')
		else:
			for conn in self.connection_list:
				x=self.connection_list[conn]
				if x[1]!=None:conn.send(text+'|')

	def EditPort(self,widget):
		text=self.obj_editport.Run()
		try:
			if int(text)>=1000:
				self.port=int(text)
				self.l_srvr.set_text(self.ip+':'+str(self.port))
				self.PrintText("[Note] :Port Changed to "+str(self.port))
			else:self.PrintText("[Note] :Enter IP above 1000 ")
		except ValueError:self.PrintText("[Warning] :Invalid IP number")
		except TypeError:pass#in case it is None , do nothing
		return True

	def GotMessage(self,source,mode):	#Evaluate messages
		sms=source.recv(1024)
		_list=sms.split('|')
		if _list==['']:
			det=self.connection_list[source]
			gobject.source_remove(det[2])	#remove IO watch
			if det[1]==None:
				text="[Note] :%s is disconnected"%det[0]
				self.PrintText(text)
			else:
				text="[Note] :%s is disconnected"%det[1]
				self.PrintText(text)
				#Notify the same to all
				text=[4,0,code.Encode(det[1])]
				self.Send2All(str(text))
				del self.userlist[code.Encode(det[1])]	#delete him/her from online user list
				self.RemoveUser(det[1])	#Remove user from tree view.
			del self.connection_list[source]	#remove him from main list
			return False

		else:	#Proper message process it 
			for pac in _list:
				if not pac:continue
				else:
					_pac=eval(pac)
					if not _pac[0]:#connection
						if _pac[1]==2:
							det=self.connection_list[source]
							text="[Note] :%s is disconnected "%det[0]
							self.PrintText(text)
							gobject.source_remove(det[2])
							del self.connection_list[source]
					if _pac[0]==1:	#registration
						if DB.Insert((code.Decode(_pac[1][0]),code.Decode(_pac[1][1]),code.Decode(_pac[1][2]))):
							self.PrintText("[Note] :"+code.Decode(_pac[1][0])+" Registered .")
							source.send("[1,1]|")
							self.newusermodel.append([code.Decode(_pac[1][1])])
						else:
							source.send("[1,0]|")
					elif _pac[0]==2:	#login
						uname=code.Decode(_pac[1][0])
						for conn in self.connection_list:
							x=self.connection_list[conn]
							if x[1]==uname:#already logged in send messaged login failed
								source.send("[2,0]|")
								return True
						passwd=code.Decode(_pac[1][1])
						if DB.Check((uname,passwd)):
							self.PrintText("[UPDATE] :"+uname+" joined")
							text=[2,1,str(code.Encode(uname))]
							source.send(str(text)+"|")
							print uname
							self.connection_list[source][1]=uname
							self.usermodel.append([uname])
							self.userlist[_pac[1][0]]=code.Encode(self.connection_list[source][0])
							l=self.connection_list[source]
							print l[0]
							ip=code.Encode(l[0])
							obj=PchatGUI(self.myname,uname,source)
							self.connected_pchat[uname]=obj	#create a private chat box for him
							for conn in self.connection_list:
								if conn!=source:
									try:conn.send(str([4,1,_pac[1][0],ip])+"|")
									except:pass
						else:source.send("[2,0]|")

					elif _pac[0]==3:	#received sms[3,uname,sms]
						self.PrintText(code.Decode(_pac[1])+" : "+code.Decode(_pac[2]))
						self.Send2All(str(_pac),code.Decode(_pac[1]))
						
					elif _pac[0]==5:	#request for log out
						name=self.connection_list[source][1]
						#don't send messages or updates
						self.PrintText("[Update] :"+name+" logged out")
						text=[4,0,code.Encode(name)]
						self.connection_list[source][1]=None
						del self.userlist[code.Encode(name)]
						self.connected_pchat[name].destroy()
						del self.connected_pchat[name]
						for conn in self.connection_list:
							if conn!=source:conn.send(str(text)+"|")
						self.RemoveUser(name)	#remove user from tree view .
					elif _pac[0]=='P':
						text=code.Decode(_pac[1])
						uname=self.connection_list[source][1]
						self.connected_pchat[uname].ShowMessage(text)
		return True
	
	def PrivateChat(self,treeview,path,column):
		iter=self.usermodel.get_iter(path)
		uname=self.usermodel.get_value(iter,0)
		self.connected_pchat[uname].Run()

	def RemoveUser(self,uname):
		iter=self.usermodel.get_iter(0)	#iter for 0 th row.
		while iter:	#if no row exists iter will be None == end of the tree view
			if uname==self.usermodel.get(iter,0)[0]:	#we had only one column
				self.usermodel.remove(iter)	#remove user from tree view
				return True
			iter=self.usermodel.iter_next(iter)
		return False

	def SendMessage(self,widget):
		text=self.send_sms.get_text()
		if not text:return True
		else:
			self.PrintText(self.myname+' :'+text)
			text=code.Encode(text)
			self.Send2All(str([3,code.Encode(self.myname),text]))	#[3,uname,sms]
			self.send_sms.set_text('')
		return True
	
	def ClearField(self,widget):
		self.send_sms.set_text('')
		return True

	def ClearView(self,widget):
		self.text_buffer.set_text('')
		return True

	def PrintText(self,text):
		enditer=self.text_buffer.get_end_iter()
		self.text_buffer.insert(enditer,text+'\n')
		return True

def findip():
	ip=[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
	if not ip:return '127.0.0.1'
	else:return ip[0]

Server()
gtk.main()


#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
