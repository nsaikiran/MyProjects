
#Creates Dialog boxes
#DO NOT EDIT
##(c) ChatRoom Team (team-09 SG-06 Batch 2010)

#Setting dialogbox classes so that we can instantiate them .

import gtk
import Messaging as code
#for all gtk reference pygtk-2.0 tutorials and pygtktutorial by Andrew Steele .
class DialogBox():	#reference pygtk-2.0 tutorials 67
	def __init__(self,title,parent):
		self.dialog = gtk.Dialog(title,parent,gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
		self.dialog.set_default_size(150,100)
		
	def Run(self):
		pass


class Dialog_EditPort(DialogBox):
	def __init__(self,parent):
		DialogBox.__init__(self,"Edit Port",parent)
		box=gtk.HBox(False,0)
		label=gtk.Label("Port Number : ")
		self.entry=gtk.Entry()
		box.pack_start(label,False,False,0)
		box.pack_start(self.entry,False,False,0)
		self.dialog.vbox.pack_start(box,False,False,0)
		
	def Run(self):
		self.dialog.show_all()
		res=self.dialog.run()
		if res==gtk.RESPONSE_OK:
			text=self.entry.get_text()
		else:
			text=None
		self.dialog.hide()
		return text

class Dialog_LogIn(DialogBox):
	def __init__(self,parent):
		DialogBox.__init__(self,'Log In',parent)
		table = gtk.Table(2,2,0)
		label1=gtk.Label("Username :")
		label2=gtk.Label("Password :")
		self.uname=gtk.Entry()
		self.pword=gtk.Entry()
		self.pword.set_visibility(False)
		table.attach(label1,0,1,0,1)
		table.attach(label2,0,1,1,2)
		table.attach(self.uname,1,2,0,1)
		table.attach(self.pword,1,2,1,2)
		self.dialog.vbox.pack_start(table,False,False,0)
	def Run(self):
		self.dialog.show_all()
		res=self.dialog.run()
		if res==gtk.RESPONSE_OK:
			result=[self.uname.get_text(),self.pword.get_text()]
		else:
			result=[]
		self.dialog.hide()
		return result

class Dialog_Register(DialogBox):
	def __init__(self,parent):
		DialogBox.__init__(self,'Register',parent)
		table = gtk.Table(3,2,0)
		label1=gtk.Label("Name :")
		label2=gtk.Label("Username :")
		label3=gtk.Label("Password :")
		self.name=gtk.Entry()
		self.uname=gtk.Entry()
		self.pword=gtk.Entry()
		self.pword.set_visibility(False)
		table.attach(label1,0,1,0,1)
		table.attach(label2,0,1,1,2)
		table.attach(label3,0,1,2,3)
		table.attach(self.name,1,2,0,1)
		table.attach(self.uname,1,2,1,2)
		table.attach(self.pword,1,2,2,3)
		self.dialog.vbox.pack_start(table,False,False,0)

	def Run(self):
		self.dialog.show_all()
		res=self.dialog.run()
		if res==gtk.RESPONSE_OK:
			result=[self.name.get_text(),self.uname.get_text(),self.pword.get_text()]
		else:
			result=[]
		self.dialog.hide()
		return result

class Dialog_PrivateChat(gtk.Window):
	def __init__(self,myname,uname,send_conn):
		gtk.Window.__init__(self)
		self.uname=uname
		self.myname=myname
		self.send_conn=send_conn	#private connection b/w clients to share (send only) text .
		self.set_title(myname+" and "+uname)
		self.set_border_width(20)
		box=gtk.VBox(False,0)

		lable=gtk.Label("Enter text :")
		self.sms=gtk.Entry()
		view=gtk.TextView()
		self.buffer=view.get_buffer()
		view.set_editable(False)
		view.set_cursor_visible(False)
		view.set_wrap_mode(gtk.WRAP_WORD)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		sw.add(view)
		frame=gtk.Frame('View Messages')
		frame.add(sw)

		self.send_button=gtk.Button('Send')
		self.clear_button=gtk.Button('Clear')

		boxx=gtk.HBox(False,1)
		boxx.pack_start(lable,False,False,0)
		boxx.pack_start(self.sms,False,False,0)
		boxy=gtk.HButtonBox()
		boxy.set_layout(gtk.BUTTONBOX_END)
		boxy.add(self.send_button)
		boxz=gtk.HButtonBox()
		boxz.set_layout(gtk.BUTTONBOX_END)
		boxz.add(self.clear_button)

		box.pack_start(boxx,False,False,0)
		box.pack_start(boxy,False,False,0)
		box.pack_start(frame,True,True,0)
		box.pack_start(boxz,False,False,0)
		self.add(box)
		
		self.send_button.connect('clicked',self.Send)
		self.sms.connect('activate',self.Send)
		self.clear_button.connect('clicked',self.Clear)
		self.connect('delete-event',self.Close)#delete-event plays very curcial role
		self.set_destroy_with_parent(True)
		
	def Run(self):
		self.show_all()

	def Close(self,widget,x):
		self.hide()
		return True	#stop destroying it refer below

	def ShowMessage(self,text):
		print text
		self.PrintText(self.uname+' :'+text)
		self.show_all()

	def PrintText(self,text):
		iter=self.buffer.get_end_iter()
		self.buffer.insert(iter,text+'\n')

	def Send(self,widget):
		text=self.sms.get_text()
		if not text:return True
		self.sms.set_text('')
		self.PrintText(self.myname+' :'+text)
		text=code.Encode(text)
		sms=['P',text]
		if self.send_conn==None:pass
		else:
			#self.send_conn.ShowMessage(text)
			self.send_conn.send(str(sms)+'|')	#if  socket connection do it
		return True

	def Clear(self,widget):
		self.buffer.set_text('')
		return True
"""
important ::
/* If you return FALSE in the "delete_event" signal handler,
     * GTK will emit the "destroy" signal. Returning TRUE means
     * you don't want the window to be destroyed.
     * This is useful for popping up 'are you sure you want to quit?'
     * type dialogs. */
"""

"""
Basically dialog box is a predefined window object that has a vbox widget inserted into it . So , if we want to insert anything into dialog box , we need to insert the same into vbox of dialog box. 
"""

#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
