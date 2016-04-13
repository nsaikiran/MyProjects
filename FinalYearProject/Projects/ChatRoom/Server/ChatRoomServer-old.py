import ChatRoomServerGui as Gui
import socket,gtk,gobject
import Messaging as code
from DataBase import DB

class Server(Gui.ServerGUI):
	def __init__(self):
		Gui.ServerGUI.__init__(self)

		self.server=0
		self.take_connection=1
		self.b_stop_srvr.hide()
		self.b_start_srvr.connect('clicked',self.StartServer)
		self.b_stop_srvr.connect('clicked',self.StopServer)
		self.b_close_srvr.connect('clicked',self.CloseServer)
		self.connect('destroy',self.CloseServer)
		self.b_send.connect('clicked',self.SendMessage)
		self.connection_list={}
		
	def StartServer(self,widget):
		if not self.server:
			self.sock=socket.socket()
			self.sock.bind(('localhost',self.port))
			self.sock.listen(5)
			self.server_id = gobject.io_add_watch(self.sock,gobject.IO_IN,self.accept_connection)
			widget.hide()
			self.server=1
		else:
			self.take_connection=1
			widget.hide()
		self.l_srvr_status.set_text('Serving . . ')
		self.b_stop_srvr.show()
		self.b_close_srvr.show()
	
	def StopServer(self,widget):
		self.take_connection=0
		widget.hide()
		self.b_start_srvr.show()
		self.l_srvr_status.set_text('Not accepting  . . ')
		return True

	def CloseServer(self,widget):
		self.sock.close()
		for conn in self.connection_list:
			conn.send('[9]|')	#
			conn.close()
		gtk.main_quit()

	def accept_connection(self,source,condition):	#source = self.socket , codition = IO_IN
		conn,addr=self.sock.accept()
		if self.take_connection:
			_id=gobject.io_add_watch(conn,gobject.IO_IN,self.GotMessage)
			self.connection_list[conn]=[addr[0],None,_id]
			conn.sendall('1')	#Creates error , have a look .
			self.PrintText('Accepted '+addr[0])
		else:
			self.PrintText('Rejected'+addr[0])
			conn.sendall('0')
		return True

	def GotMessage(self,source,condition):
		print 'hi'
		sms=source.recv(1024)
		print sms
		packets=sms.split('|')
		print packets
		for pac in packets:
			if not pac:continue
			print pac
			_sms=eval(pac)
			print _sms
			if _sms[0]==0:
				if _sms[1]:#[]
					uname=code.Decode(_sms[2])
					passwd=code.Decode(_sms[3])
					if DB.Check((uname,passwd)):
						source.send(str([0,1])+'|')
						self.PrintText(uname+' : joined .')
						self.connection_list[source][1]=uname
						self.send2all(str([2,1,code.Encode(uname)]))
					else:
						source.send('[0,0]|')
				else:
					sms_=[2,0,code.Encode(self.connection_list[source][1])]
					self.send2all(str(sms_))
					self.PrintText(code.Decode(_sms[2])+' logged out.')
					self.connection_list[source][1]=None
			elif _sms[0]==1:
				self.send2all(pac)
				self.PrintText(code.Decode(_sms[1])+' : '+code.Decode(_sms[2]))
			elif _sms[0]==3:
				print _sms
				if DB.Insert((code.Decode(_sms[1]),code.Decode(_sms[2]),code.Decode(_sms[3]))):
					self.PrintText(code.Decode(_sms[1])+'registered')
					source.send('[3,1]|')
				else:source.send('[3,0]|')
		
			elif _sms[0]==9:
				try:
					gobject.source_remove(self.connection_list[source][2])
				except:pass
				del self.connection_list[source]
			
		return True

	def SendMessage(self,widget):
		if not self.connection_list:pass
		else:
			sms=self.send_sms.get_text()
			if not sms:pass
			else:
				_sms=[1,code.Encode('srvr'),code.Encode(sms)]
				self.send2all(str(_sms))
				self.PrintText('srvr : '+sms)
				self.send_sms.set_text('')
		return True

	def PrintText(self,text):
		enditer=self.text_buffer.get_end_iter()
		self.text_buffer.insert(enditer,text+'\n')

	def send2all(self,text):
		for conn in self.connection_list:
			if self.connection_list[conn][1]!=None:
				conn.send(text+'|')

Server()
gtk.main()
		
