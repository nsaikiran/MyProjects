#Main program FOR CLIENT GUI
#DO NOT EDIT
#
#(c) ChatRoom Team (team-09 SG-06 Batch 2010)


import gtk

#Main for project ...
#Saikiran 

class ClientGUI(gtk.Window):
	def __init__(self):
		#create a window 
		gtk.Window.__init__(self)
		self.set_title('Chat Room Client')
		self.set_default_size(500,600)
		self.set_resizable(True)
		self.port=6380


		MainBox=gtk.HBox(False,1)
		self.set_border_width(1)
		sw=gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
		self.UserStore,self.UsersView=self.CreateTreeView()
		sw.add(self.UsersView)
		
		MainBox.pack_end(sw,True,True,2)
		MainBox.pack_end(gtk.VSeparator(),False,False,0)
		MainBox.pack_end(self.DesignFrames(),True,True,1)

		self.add(MainBox)
		self.connect('destroy',self.Close)
		self.show_all()

	def CreateTreeView(self):
		#we are creating a tree - view . To create a tree view , 
		#we have to define its structure / model . Based on that model we make tree-view. 
		store=gtk.ListStore(str)
		#Coloumn contain only string values .
		#Or that is the basic schema of the Tree Model , that contain one column of string type
		#for names in range(10):
		#	store.append(['User'+str(names)]) #add values to coloumn
		# create the TreeView using treestore (defined tree model )
		treeview = gtk.TreeView(store)
		# create the TreeViewColumn to display the data
		tvcolumn = gtk.TreeViewColumn("ChatRoom Users") #differentiate a column .
		# add tvcolumn to treeview
		treeview.append_column(tvcolumn)
		# create a CellRendererText to render the data
		cell = gtk.CellRendererText()
		# add the cell to the tvcolumn and allow it to expand over the column to render the text
		tvcolumn.pack_start(cell, True)
		# set the cell "text" attribute to saikiran's - retrieve text
		# from that column in treestore
		tvcolumn.add_attribute(cell, 'text', 0)
		# make it searchable
		treeview.set_search_column(0)
		# Allow sorting on the column
		tvcolumn.set_sort_column_id(0)
		# Allow drag and drop reordering of rows
		treeview.set_reorderable(True)
		return store,treeview

	def DesignFrames(self):
		box=gtk.VBox(False,2)
	
		#Connection frame starts here
		box_f1=gtk.VBox(False,1)
		f1=gtk.Frame('Connection')
		box1=gtk.HBox(False,1)
		label=gtk.Label('Server :')
		self.s_ip=gtk.Entry()	#note this
		self.s_ip.set_text('Enter server ip')
		
		self.port_label=gtk.Label(':'+str(self.port))	#note
		
		self.s_ip.set_editable(True)
		box1.pack_start(label,False,False,1)
		box1.pack_start(self.s_ip,True,True,1)
		box1.pack_start(self.port_label,False,False,1)

		bbox=gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_sconnect=gtk.Button('Connect')
		
		bboxx=gtk.HButtonBox()
		bboxx.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_login=gtk.Button('Log in')
		self.b_logout=gtk.Button('Log out')
		self.b_register=gtk.Button('register')
		bboxx.add(self.b_login)
		bboxx.add(self.b_logout)
		bboxx.add(self.b_register)
		self.hidable2=bboxx		
		
		#self.b_s_c_d.connect('clicked',self.addme,box_f1,bboxx)
		self.b_dconnect=gtk.Button('Disconnect')
		self.b_eport=gtk.Button('Edit Port')
		bbox.add(self.b_sconnect)	#note
		bbox.add(self.b_dconnect)	#note
		bbox.add(self.b_eport)	#note
		self.hidable1=bbox	#note
		
		
		box_f1.pack_start(box1,False,False,1)
		self.l_conn_status=gtk.Label('Not connected')
		box_f1.pack_start(self.l_conn_status,False,False,0)
		box_f1.pack_start(bbox,False,False,1)
		box_f1.pack_start(bboxx,False,False,1)
		f1.add(box_f1)
		#connection frame ends here

		f2=gtk.Frame('Messages')
		box_f2=gtk.VBox(False,1)
		box2=gtk.HBox(False,1)
		label2=gtk.Label("Enter text :")
		self.send_sms=gtk.Entry()
		box2.pack_start(label2,False,False,0)
		box2.pack_start(self.send_sms,True,True,0)

		bbox2=gtk.HButtonBox()
		bbox2.set_layout(gtk.BUTTONBOX_END)
		bbox2.set_spacing(30)
		self.b_send=gtk.Button('Send')
		self.b_clear=gtk.Button('Clear')
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
		box_for_sms=gtk.VBox(False,0)
		box_for_sms.pack_start(sw,True,True,1)
		bbox3=gtk.HButtonBox()
		bbox3.set_layout(gtk.BUTTONBOX_END)
		self.b_clear_view=gtk.Button('Clear')
		bbox3.add(self.b_clear_view)
		box_for_sms.pack_start(gtk.HSeparator(),False,False,0)
		box_for_sms.pack_start(bbox3,False,False,1)
		
		vframe.add(box_for_sms)
		box_f2.pack_start(vframe,True,True,10)

		f2.add(box_f2)

		f3=gtk.Frame('Options')
		bbox4=gtk.HButtonBox()
		bbox4.set_layout(gtk.BUTTONBOX_SPREAD)
		self.b_help=gtk.Button('Help')
		self.b_settings=gtk.Button('Settings')
		bbox4.add(self.b_settings)
		bbox4.add(self.b_help)
		f3.add(bbox4)
		
		box.pack_start(f1,False,False,1)
		box.pack_start(gtk.HSeparator(),False,False,0)
		box.pack_start(f2,True,True,1)
		box.pack_start(f3,False,False,1)
		return box

	def Close(self,widget):
		gtk.main_quit()


"""

Imp to know about cell renderers , treeview, treestore,liststore .
CellRendererText Markup in pygtk2.0 ==196 page
"""

#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
