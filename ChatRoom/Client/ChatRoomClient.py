#Main program that initiates client
#DO NOT EDIT
#
#(c) ChatRoom Team (team-09 SG-06 Batch 2010)


import socket,gobject,gtk
import ChatRoomClientGui as Gui
import Messaging as code
import Dialog
PchatGUI=Dialog.Dialog_PrivateChat

#Main class for client ...
#new code for client .... updated .

class Client(Gui.ClientGUI):
	def __init__(self):
		Gui.ClientGUI.__init__(self)
		self.Reset()
		#variable declaration
		self.connected=0
		self.allowmessage=0
		self.userlist={}	#{uname:ip}
		#variable declaration
		self.obj_editport=Dialog.Dialog_EditPort(self)
		self.obj_login=Dialog.Dialog_LogIn(self)
		self.obj_register=Dialog.Dialog_Register(self)
		self.b_logout.connect('clicked',self.LogOut)
		self.b_login.connect('clicked',self.LogIn)
		self.b_sconnect.connect('clicked',self.Connect)
		self.b_dconnect.connect('clicked',self.Disconnect)
		self.b_eport.connect('clicked',self.EditPort)
		self.b_register.connect('clicked',self.Register)
		self.b_send.connect('clicked',self.SendMessage)
		self.send_sms.connect('activate',self.SendMessage)
		self.b_clear.connect('clicked',self.ClearField)
		self.b_clear_view.connect('clicked',self.ClearView)
		self.connected_list={}	#{uname:[conn,conn_id,ip]}
		self.UsersView.connect('row-activated',self.PrivateChat)	#shows online users , double click to private chat
		
	def Connect(self,widget):
		self.ip=self.s_ip.get_text()
		List=self.ip.split('.')
		print List
		if len(List)==4:#ipv4
			for ele in List:
				try:
					if type(eval(ele))!=int:
						self.PrintText("[Warning] :Invalid IPV4 address")
						return True
				except:
					self.PrintText("[Warning] :Invalid IPV4 address")
					return True
		else:
			self.PrintText("[Warning] :Invalid IPV4 address")
			return True

		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		try:
			self.sock.connect((self.ip,self.port))
			self.conn_id=gobject.io_add_watch(self.sock,gobject.IO_IN,self.GotMessage)
		except socket.error:
			self.PrintText("[Note] :Network Error")
			self.sock.close()
			return True
		#When server is diconnected ... User wants to connect again , we want to clear connection list and destroy GUIs.
		for name in self.connected_list:
			x=self.connected_list[name]
			x[0].close()
			gobject.source_remove(x[1])
			x[3].destroy()

		#above code executed when, server disconnected .. some of private chat boxes are on. and in that case if user wants to connect again
		self.connected_list={}	#{uname:[conn,conn_id,ip]}
		self.UserStore.clear()	#clear
		return True

	def Register(self,widget):
		result=self.obj_register.Run()#[name,uname,password]
		print result
		if not result:pass
		else:	#do some work ...
			if not result[0] or not result[1] or not result[2]:self.PrintText("[Warning]: Please fill all fields in registration area.")
			else:	#process it further
				self.sock.send(str([1,[code.Encode(result[0]),code.Encode(result[1]),code.Encode(result[2])]])+'|')
		return True

	def Reset(self):
		self.b_logout.hide()
		self.b_sconnect.show()
		self.b_eport.show()
		self.hidable1.show()
		self.hidable2.hide()
		self.b_dconnect.hide()
		self.UserStore.clear()
		self.b_settings.hide()

	def LogIn(self,widget):
		result=self.obj_login.Run()#[uname,password]
		print result
		if not result:pass
		else:	#do some work
			if not result[0] or not result[1]:self.PrintText("[Warning]: Please fill all fields in login area .")
			else:	#process it further.
				sms=[2,[code.Encode(result[0]),code.Encode(result[1])]]
				self.sock.send(str(sms)+'|')
		return True

	def LogOut(self,widget):
		self.sock.send("[5]|")	#5->request for logout
		self.PrintText("[Note] :Successfully logged out from"+str(self.ip))
		self.allowmessage=0
		self.hidable1.show()
		self.b_logout.hide()
		self.b_login.show()
		self.b_register.show()
		self.b_settings.hide()
		#Close all private chat connections, i/o ids and destroy GUIs
		for name in self.connected_list:
			x=self.connected_list[name]
			if name!='admin':
				x[0].close()
				gobject.source_remove(x[1])
			x[3].destroy()
		gobject.source_remove(self.pchatserver_id)
		self.pchatsock.close()

	def Disconnect(self,widget):
		self.l_conn_status.set_text("Disconnected . .")
		gobject.source_remove(self.conn_id)
		self.sock.send("[0,2]|")
		self.sock.close()
		self.PrintText('[Note]: Disconnected from '+str(self.ip))
		self.Reset()
		self.userlist={}


	def EditPort(self,widget):
		text=self.obj_editport.Run()
		try:
			if int(text)>=1000:
				self.port=int(text)
				self.port_label.set_text(str(':'+str(self.port)))
				self.PrintText("[Note]: Port Changed to "+str(self.port))
			else:self.PrintText("[Warning]: Enter IP above 1000 ")
		except ValueError:self.PrintText("[Warning]: Invalid IP number")
		except TypeError:pass#in case it is None , do nothing
		return True

	def GotMessage(self,source,mode):	#GotMessage From only server
		sms=source.recv(1024)
		print sms
		_list=sms.split('|')
		print _list
		if _list==['']:
			#means socket(server / private clients) closed without prior message . Stop IO watch
			gobject.source_remove(self.conn_id)
			self.PrintText("[Note] :Server Disconnected")
			self.sock.close()
			self.Reset()
			self.allowmessage=0
			#Destroy only admin GUI because some people may still be on-line even server disconnected
			self.connected_list['admin'][3].destroy()
			return False
		else:
			for pac in _list:
				if not pac:continue
				else:
					_pac=eval(pac)
					if not _pac[0]:	#all about connection
						if _pac[1]==1:
							self.PrintText("[Note] :Successfully Connected to %s"%self.ip)
							self.l_conn_status.set_text("Connected . .")
							self.b_sconnect.hide()
							self.b_dconnect.show()
							self.b_eport.hide()
							self.hidable2.show()
						elif not _pac[1]:
							self.PrintText("[Note] :Connection Rejected %s"%self.ip)
							gobject.source_remove(self.conn_id)
							self.sock.close()
							return False
					elif _pac[0]==1:	#registration
						if _pac[1]==1:
							self.PrintText("[Note] :Registration Successful")
						else:
							self.PrintText("[Note] :Registration Failed")
					elif _pac[0]==2:	#log in
						if _pac[1]==1:	#success
							self.myname=code.Decode(_pac[2])
							self.PrintText("[Note] :Log In Successful as "+self.myname)
							self.hidable1.hide()
							self.b_register.hide()
							self.b_login.hide()
							self.b_logout.show()
							self.b_settings.show()	#all user to change settings
							self.allowmessage=1	#allow sending messages
							#initiate private chat server
							obj=PchatGUI(self.myname,'admin',self.sock)
							self.connected_list['admin']=[self.sock,self.conn_id,self.ip,obj]
							self.StartPChatServer()

						else:self.PrintText("[Note] :Log In Failed")

					elif _pac[0]==3:	#received sms
						self.PrintText(code.Decode(_pac[1])+": "+code.Decode(_pac[2]))
					elif _pac[0]==4:
						if _pac[1]==0:	#userloggedout
							uname=code.Decode(_pac[2])
							self.PrintText("[Update] :"+uname+" logged out")
							del self.userlist[uname]
							#delete user from online list .. pending
							self.RemoveUser(uname)
							if uname in self.connected_list:
								gobject.source_remove(self.connected_list[uname][1])
								self.connected_list[uname][3].destroy()
								del self.connected_list[uname]

						elif _pac[1]==1:	#userlogged in
							uname=code.Decode(_pac[2])
							print uname
							print "ip",code.Decode(_pac[3])
							self.userlist[uname]=code.Decode(_pac[3])
							self.UserStore.append([uname])
							self.PrintText("[Update] :"+uname+" joined")
						else:	#userlist 
							for w in _pac[2]:
								self.userlist[code.Decode(w)]=code.Decode(_pac[2][w])
							self.UserStore.clear()
							for w in self.userlist:self.UserStore.append([w])

					elif _pac[0]=='P':
						text=code.Decode(_pac[1])
						self.connected_list['admin'][3].ShowMessage(text)
			return True

	def RemoveUser(self,uname):
		try:
			iter=self.UserStore.get_iter(0)	#iter for 0 th row.
		except ValueError:return
		while iter:	#if no row exists iter will be None == end of the tree view
			if uname==self.UserStore.get(iter,0)[0]:	#we had only one column
				self.UserStore.remove(iter)	#remove user from tree view
				return True
			iter=self.UserStore.iter_next(iter)
		return False
	
	def StartPChatServer(self):
		self.pchatsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.pchatsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		myip=findip()
		print myip
		try:
			self.pchatsock.bind((myip,self.port))
		except socket.error:
			self.PrintText('[Warning] :You can not initiate private chat. Because adress already in use')
			self.LogOut(None)
			self.Reset()
			self.pchatsock.close()
			return True
		self.pchatsock.listen(5)
		self.pchatserver_id=gobject.io_add_watch(self.pchatsock,gobject.IO_IN,self.accept_pchat_connection)
		return True

	def accept_pchat_connection(self,source,mode):
		#self.userlist	gives online users .. {uname:ip}
		#self.connected_list {uname:[conn,conn_id,ip,GUI]}
		print 'received \n\n'
		conn,addr=self.pchatsock.accept()
		for user in self.userlist:
			if self.userlist[user]==addr[0]:
				obj=PchatGUI(self.myname,user,conn)
				id_=gobject.io_add_watch(conn,gobject.IO_IN,self.GotPrivateMessage)
				self.connected_list[user]=[conn,id_,addr[0],obj]	#outer username and conn
		return True

	def GotPrivateMessage(self,source,mode):
		text=source.recv(1024)
		_list=text.split('|')
		for user in self.connected_list:
			if self.connected_list[user][0]==source:
				sender=user
		if _list==['']:
				gobject.source_remove(self.connected_list[sender][1])
				self.connected_list[sender][3].destroy()
				print 'done'
				del self.connected_list[sender]
				return False
		else:
			for pac in _list:
				if not pac:continue
				else:
					list_=eval(pac)
					if list_[0]=='P':	#private chat
						sms=code.Decode(list_[1])
						self.connected_list[sender][3].ShowMessage(sms)
		return True

	def PrivateChat(self,treeview,path,column):
		if not self.allowmessage:return True
		iter=self.UserStore.get_iter(path)
		uname=self.UserStore.get_value(iter,0)
		if uname in self.connected_list:
			self.connected_list[uname][3].Run()
		else:
			ip=self.userlist[uname]
			sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			try:
				sock.connect((ip,self.port))
			except:
				print 'Connecion failed'
				return True
			id_=gobject.io_add_watch(sock,gobject.IO_IN,self.GotPrivateMessage)
			obj=PchatGUI(self.myname,uname,sock)
			self.connected_list[uname]=[sock,id_,ip,obj]
			print self.connected_list
			obj.Run()

	def SendMessage(self,widget):
		if not self.allowmessage:return True
		text=self.send_sms.get_text()
		if not text:return True
		else:
			self.PrintText(self.myname+' :'+text)
			text=code.Encode(text)
			self.sock.send(str([3,code.Encode(self.myname),text])+"|")	#[3,uname,sms]
			self.send_sms.set_text('')
		return True

	def PrintText(self,text):
		enditer=self.text_buffer.get_end_iter()
		self.text_buffer.insert(enditer,text+'\n')
		return True

	def ClearField(self,widget):
		self.send_sms.set_text('')
		return True

	def ClearView(self,widget):
		self.text_buffer.set_text('')
		return True

	def Close(self,widget):#Override method . . 
		if self.allowmessage:
			#Close all private chat connections, i/o id's and destroy GUI's
			for name in self.connected_list:
				x=self.connected_list[name]
				gobject.source_remove(x[1])
				x[0].close()
				x[3].destroy()
			self.pchatsock.close()
			gobject.source_remove(self.pchatserver_id)
		gtk.main_quit()
def findip():
	ip=[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
	if not ip:return '127.0.0.1'
	else:return ip[0]

def main():
	Client()
	gtk.main()
if __name__=='__main__':
	main()


#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
