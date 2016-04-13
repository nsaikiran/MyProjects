#Main program for server GUI. This creates server GUI part.
#DO NOT EDIT
##(c) ChatRoom Team (team-09 SG-06 Batch 2010)

import gtk

class ServerGUI(gtk.Window):
	
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title('ChatRoomServer')
		self.set_default_size(500,600)
		self.port=6380
		self.connect('destroy',self.CloseWindow)
	
		MBox=gtk.HBox(False,0)
		sw,self.usermodel,self.UserListView=self.CreateUserList('ChatRoom Users')
		MBox.pack_end(sw,True,True,0)
		MBox.pack_end(gtk.VSeparator(),False,False,0)
		
		opt=gtk.VBox(False,0)
		opt.pack_start(self.ServerPanel(),False,False,0)
		opt.pack_start(self.MessagingPanel(),True,True,0)
		opt.pack_start(self.MoniteringPanel(),False,False,0)
		MBox.pack_end(opt)
		sw,self.newusermodel,self.NewUserListView=self.CreateUserList('Total Users')
		MBox.pack_end(gtk.VSeparator(),False,False,0)
		MBox.pack_end(sw,True,True,0)
		self.add(MBox)
		self.show_all()

	def CreateUserList(self,head):
		model=gtk.ListStore(str)
		#for user in range(10):
		#	model.append(['Client'+str(user)])
		view=gtk.TreeView(model)
		render=gtk.CellRendererText()
		vcolumn=gtk.TreeViewColumn(head)
		view.append_column(vcolumn)
		vcolumn.pack_start(render,True)
		vcolumn.add_attribute(render,'text',0)
		# make it searchable
		view.set_search_column(0)
		# Allow sorting on the column
		vcolumn.set_sort_column_id(0)
		# Allow drag and drop reordering of rows
		view.set_reorderable(True)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)#makes scroll bars visible when child is larger than it.
		sw.add(view)
		return sw,model,view

	def ServerPanel(self):

		f1=gtk.Frame('Server Panel')
		vbox1=gtk.VBox(False,2)
		self.l_srvr=gtk.Label('10.4.6.193'+':'+str(self.port))	#note
		bbox=gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_start_srvr=gtk.Button('Start')	#note
		self.b_stop_srvr=gtk.Button('Stop')	#note
		self.b_close_srvr=gtk.Button('close')	#note
		self.b_editport=gtk.Button('Edit port')
		bbox.add(self.b_start_srvr)
		bbox.add(self.b_stop_srvr)
		bbox.add(self.b_close_srvr)
		bbox.add(self.b_editport)
		self.l_srvr_status=gtk.Label('Not Serving')
		vbox1.pack_start(self.l_srvr,False,False,1)
		vbox1.pack_start(bbox,False,False,1)
		vbox1.pack_start(self.l_srvr_status,False,False,0)
		f1.add(vbox1)
		
		return f1

	def MessagingPanel(self):
		f2=gtk.Frame('Messages')

		box_f2=gtk.VBox(False,1)
		box2=gtk.HBox(False,1)
		label2=gtk.Label("Enter text :")
		self.send_sms=gtk.Entry()	#note
		box2.pack_start(label2,False,False,0)
		box2.pack_start(self.send_sms,True,True,0)

		bbox2=gtk.HButtonBox()
		bbox2.set_layout(gtk.BUTTONBOX_END)
		bbox2.set_spacing(30)
		self.b_send=gtk.Button('Send')	#note
		self.b_clear=gtk.Button('Clear')	#note
		bbox2.add(self.b_send)
		bbox2.add(self.b_clear)
		box_f2.pack_start(box2,False,False,0)
		box_f2.pack_start(bbox2,False,False,0)
		
		view=gtk.TextView()
		view.set_editable(False)
		view.set_cursor_visible(False)
		view.set_wrap_mode(gtk.WRAP_WORD)
		self.text_buffer=view.get_buffer()	#note
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		sw.add(view)
		vframe=gtk.Frame('View Messages')
		vframe.add(sw)
		box_f2.pack_start(vframe,True,True,10)
		bbox3=gtk.HButtonBox()
		bbox3.set_layout(gtk.BUTTONBOX_END)
		self.b_clearview=gtk.Button('Clear')
		bbox3.add(self.b_clearview)
		box_f2.pack_start(bbox3,False,False,0)
		f2.add(box_f2)

		return f2

	def MoniteringPanel(self):

		vbox=gtk.VBox(False,0)

		f=gtk.Frame('Total Users')
		bbox=gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_deleteuser=gtk.Button('Delete User')	
		bbox.add(self.b_deleteuser)
		f.add(bbox)

		f2=gtk.Frame('Options')
		bbox2=gtk.HButtonBox()
		bbox2.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_help=gtk.Button('Help')	#note
		self.b_settings=gtk.Button('Settings')	#note
		bbox2.add(self.b_settings)
		bbox2.add(self.b_help)
		f2.add(bbox2)
		
		vbox.pack_start(f,False,False,0)
		vbox.pack_start(f2,False,False,0)
		return vbox
	def CloseWindow(self,widget):gtk.main_quit()

if __name__=='__main__':
	ServerGUI()
	gtk.main()


#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
