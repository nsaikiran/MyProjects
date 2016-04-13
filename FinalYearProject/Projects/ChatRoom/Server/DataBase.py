#One of programs for  server section of chatroom.
#Connects to MySQL server running in localhost, and execute queries.
#DO NOT EDIT
##(c) ChatRoom Team (team-09 SG-06 Batch 2010)

import Variables
mysqlusername=Variables.mysqlusername
mysqlpassword=Variables.mysqlpassword
try:
	import MySQLdb as sql
except ImportError:
	print "No Module named MySQLdb, It is required"
	exit()	#It means exit from python (Whole program will exit)
try:
	db=sql.connect('localhost',mysqlusername,mysqlpassword,'mysql')	#database mysql will always be there. But we are not supposed to use it.
	print "MySQL connection : success"
except:
	print "Change username and password for MySQL server in Variables.py"
	exit()

cursor=db.cursor()
try:
	cursor.execute("use ChatRoom")	#change database
	print "Database Changed to ChatRoom"
except:
	print "No database"
	cursor.execute("create database ChatRoom")
	cursor.execute("use ChatRoom")
	cursor.execute("create table ChatRoomUser(name char(20) not null,usrname char(20) not null,passwd char(20) not null)")
	query="INSERT INTO ChatRoomUser VALUES('%s','%s','%s')"%('admin','admin','admin')	#including admin
        cursor.execute(query)

class DataBase: #Can make operations on table ChatRoomUser
    def __init__(self,db):
        self.db=db
        self.cursor=db.cursor()
        
    def Insert(self,Tuple):# Tuple (name,uname,passwd ) Nothinig but register
        #Check if user exists
        print Tuple
        query="SELECT name FROM ChatRoomUser WHERE usrname='%s'" %(Tuple[1])
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if not result:
           query="INSERT INTO ChatRoomUser VALUES('%s','%s','%s')"%Tuple
           self.cursor.execute(query)
           #commit the result
           db.commit()
	   return 1
        else:
            print "\nSorry ! Change user name \n"
	    return 0

    def Check(self,Tuple):
        query="SELECT passwd FROM ChatRoomUser WHERE usrname='%s'"%Tuple[0]
        self.cursor.execute(query)
        #we assume there exist one solution 
        result=self.cursor.fetchall()
        print 'result',result
        if not result:
            print 'Username doesnot exist'
            return 0
        if result[0][0]==Tuple[1]:
            print 'Log In successful'
            return 1
        else:
            print 'Invalid password'
            return 0
    def ChangePassword(self,Tuple):#(usr name , pass , new pass)
        query="SELECT passwd FROM ChatRoomUser WHERE usrname='%s'"%(Tuple[0])
        self.cursor.execute(query)
        result=self.cursor.fetchall()
        if not result:
            print 'No User exist'
            return 0
        #print result[0][0]
        if result[0][0]==Tuple[1]:
            query="UPDATE ChatRoomUser SET passwd='%s' WHERE usrname='%s'"%(Tuple[2],Tuple[0])
            self.cursor.execute(query)
            print 'Successfully changed password'
            return 1
        else:
            print 'Invalid Password'
            return 0
        
    def GetAll(self):
	query="SELECT usrname FROM ChatRoomUser"
	self.cursor.execute(query)
	return self.cursor.fetchall()

    def Name(self,uname):
	self.cursor.execute("SELECT name From ChatRoomUser where usrname='%s'"%(uname))
	return self.cursor.fetchall()

    def CloseDB(self):
        self.db.close()
        
DB=DataBase(db)
#Pre - prossess or validate the tuple before processing .
if __name__=='__main__':
	DB.Insert(('kingston','123','456'))

	query="SELECT * FROM ChatRoomUser"
	cursor.execute(query)
	result=cursor.fetchall()
	for re in result:print re

	DB.Check(('bobby','banana'))
	DB.ChangePassword(('kingston','123','456'))
	DB.CloseDB()

#(c)	N.SAI KIRAN
#	V.KALPAVALLI
#	B.NAVEEN
#	V.SUPRIYA
