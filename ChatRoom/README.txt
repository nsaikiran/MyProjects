====================
CHAT ROOM v1.0
====================

Required modules in python2.x / python 3.x to be installed for both SERVER and CLIENT section.

1).pygtk			
2).pygobject			

Additional requirement for SERVER section:
1).MySQLdb-python-1.2.3		-- python API for MySQL

==) For UNIX family operating systems pygtk,pygobject are in-built . For these OSs MySQLdb should be installed.
==) For windows OS all above three should be installed, along with their other dependencies.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SOFTWARES:
1).MySQL server

for SERVER section only.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

************************************************
INSTALLING PYGTK IN WINDOWS OPERATING SYSTEM:

1).Follow instructions given in https://git.gnome.org/browse/pygtk/ to install pygtk and pycairo
************************************************

----------------------------------
MAKE SURE YOU HAVE ALL THESE FILES
=--------------------------------=
SERVER section:
1).ChatRoomServer.py / ChatRoomServer.pyc
2).ChatRoomServerGui.py /ChatRoomServerGui.pyc
3).Dialog.py	/Dialog.pyc
4).DataBase.py /DataBase.pyc
5).Messaging.py	/ Messaging.pyc
5).Variables.py

CLIENT section:
1).ChatRoomClient.py / ChatRoomClient.pyc
2).ChatRoomClientGui.py /ChatRoomClientGui.pyc
3).Dialog.py / Dialog.pyc
4).Messaging.py / Messaging.pyc

		= Usage =
ServerSection:
--------------
1).for UNIX family OSs
	- Open 'variables.py' and check sqlusername,sqlpassword values.Provide correct sqlusername,sqlpassword for database access.
	- Start MySQL server
	- double click on 'runserver.sh' if it is not working chage its permissions to 'allow execute'.
	- click on start button to start serving.
2).for Windows family OSs
	- Open 'Variables.py' and check mysqlusername,mysqlpassword values.Provide correct mysqlusername,mysqlpassword for database access.
	- Start MySQL server
	- run ChatRoomServer.py with IDLE python		(we will generate a .exe/.pyw file)
	- click on start button to start serving

Client Section:
---------------
1).for UNIX family OSs:
	- double click on 'runclient.sh' if it is not working chat its permissions to 'allow execute'.
	- enter a valid server ip to connect
2).for Windows:
	- run ChatRoomClient.py with IDLE python.		(we will generate a .exe/.pyw file )



