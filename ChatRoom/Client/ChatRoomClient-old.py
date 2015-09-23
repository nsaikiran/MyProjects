import socket,gobject,gtk
import ChatRoomClientGui as Gui
import Messaging as code


class Client(Gui.ClientGUI):
	def __init__(self):
		Gui.ClientGUI.__init__(self)
		self.hidable.hide()
		self.b_dconnect.hide()
		self.b_logout.hide()
		self.b_sconnect.connect('clicked',self.ConnectServer)
		self.b_sport.connect('clicked',self.changeport)
		self.b_dconnect.connect('clicked',self.DisconnectServer)
		self.b_send.connect('clicked',self.SendMessage)
		self.b_login.connect('clicked',self.LogIn)
		self.b_logout.connect('clicked',self.LogOut)
		self.b_register.connect('clicked',self.Register)
		self.connect('destroy',self.Close)
		self.connected=0
		self.allowmessage=0

	def ConnectServer(self,widget):

		self.ip=self.s_ip.get_text()
		print self.ip
		List=self.ip.split('.')
		print List
		if len(List)==4:#ipv4
			for ele in List:
				if type(eval(ele))!=int:
					return
		else:
			return 
		print 'done'

		self.sock=socket.socket()
		enditer=self.text_buffer.get_end_iter()
		try:
			self.sock.connect((self.ip,self.port))
			if eval(self.sock.recv(10)):	#Create error in future . Have a look 
				self.l_conn_status.set_text('Connected .')
				self.connected=1
				self.text_buffer.set_text('Successfully connected to '+self.ip+'\n')
				self.connection_id=gobject.io_add_watch(self.sock,gobject.IO_IN,self.GETMessage)	#close this with window ... write code for this .
				widget.hide()
				self.b_dconnect.show()
				self.hidable.show()
			else:
				self.text_buffer.insert(enditer,'Connection not accepted :'+self.ip+'\n')
				self.sock.close()
		except socket.error:
			self.text_buffer.insert(enditer,'Network Error\n')
			self.sock.close()
			return

	def DisconnectServer(self,widget):
		self.sock.send('[9]|')
		self.sock.close()
		widget.hide()
		self.b_sconnect.show()
		self.hidable.hide()
		self.l_conn_status.set_text('Not connected')
		if self.allowmessage:self.PrintText('Logged Out')
		self.PrintText('Disconnected from '+self.ip)
		self.allowmessage=0
		self.connected=0

	def LogIn(self,widget):
		self.username,self.passwd=Gui.DialogBox(self).Run()
		if not self.username:
			return True
		else:
			sms=[0,1,code.Encode(self.username),code.Encode(self.passwd)]
			self.sock.send(str(sms)+'|')
		return True

	def LogOut(self,widget):
		if self.allowmessage:
			self.PrintText('Logged Out')
			_sms=[0,0,code.Encode(self.username)]
			widget.hide()
			self.b_login.show()
			self.sock.send(str(_sms)+'|')
			self.allowmessage=0
		return True
		
	def changeport(self,widget):
		pass

	def GETMessage(self,source,condition):
		sms=self.sock.recv(1024)
		print sms
		packets=sms.split('|')
		print packets
		for pac in packets:
			if pac=='':continue
			list_=eval(pac)
			if list_[0]==0:
				if list_[1]:
					self.PrintText('Log In successful.')
					self.allowmessage=1
					self.b_login.hide()
					self.b_logout.show()
				else:
					self.PrintText('Log In Failed [Change Username]')
			elif list_[0]==1:#[1, uname ,sms] got sms
				self.PrintText(code.Decode(list_[1])+' > '+code.Decode(list_[2]))
			elif list_[0]==2:#[2, 0/1 , uname ]
				if list_[1]:#1
					self.PrintText(code.Decode(list_[2])+' joined .')
				else:#0
					self.PrintText(code.Decode(list_[2])+' logged out .')
			elif list_[0]==3:
				if list_[1]:
					self.PrintText('Registered Succeesfully')
				else:self.PrintText('Registration Failed\n')
			elif list_[0]==9:
				self.PrintText('Server Closed\n')
				gobject.source_remove(self.connection_id)
		return True

	def SendMessage(self,widget):
		if not self.allowmessage:pass
		else:
			sms=self.send_sms.get_text()
			if not sms:pass
			else:
				_sms=[1,code.Encode(self.username),code.Encode(sms)]
				self.sock.send(str(_sms)+'|')
				self.send_sms.set_text('')
		return True

	def Register(self,widget):
		Tuple=Gui.Dialog_Register(self).Run()
		print Tuple
		if not Tuple[0] or not Tuple[1]:
			return True
		else:
			print 'sent'
			sms=[3,code.Encode(Tuple[0]),code.Encode(Tuple[1]),code.Encode(Tuple[2])]
			print sms
			self.sock.send(str(sms)+'|')
		return True

	def PrintText(self,text):
		enditer=self.text_buffer.get_end_iter()
		self.text_buffer.insert(enditer,text+'\n')

	def Close(self,widget):
		self.sock.send('[9]|')
		try:
			gobject.source_remove(self.connection_id)
		except:pass
		gtk.main_quit()
Client()
gtk.main()
