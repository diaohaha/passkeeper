#! /usr/bin/env python
# -*- coding: utf-8 -*-

#author:gaoda
#date:2012.6.8
#filename:passkeeper.core
#descirbe:a keeper for your all kinds of password

from sqlalchemy import *
from sqlalchemy.orm import *
import string
import sys
import argparse

class pwd(object):
	def _init_(self,where,user,pwd):
		self.where=where
		self.user=user
		self.pwd=pwd
		
engine = create_engine('sqlite:///pwddb.db')
metadata=MetaData(engine)
gaoda_pwd_table=Table(
	'pwd',metadata,
	Column('where',String,primary_key=True),
	Column('user',String),
	Column('pwd',String)
	)
metadata.create_all(engine)
mapper(pwd,gaoda_pwd_table)	
session=sessionmaker(bind=engine)
session=create_session()

def look():
	i=0
	print "************************************************"
	print "where".rjust(8),"|","user".rjust(12),"|","pwd".rjust(20)
	print "************************************************"
	for temp_pwd in session.query(pwd).all():
		print str(temp_pwd.where).rjust(8),"|",str(temp_pwd.user).rjust(12),"|",str(temp_pwd.pwd).rjust(20)
		i=i+1
	if i==0:
		print "no record!"
	print "************************************************"	

def add():
	temp_pwd=pwd()
	temp_pwd.where=raw_input("where:")
	temp_pwd.user=raw_input("user:")
	temp_pwd.pwd=raw_input("password:")
	session.add(temp_pwd)
	session.flush()
def delete():
	temp_where=raw_input("the password in where:")
	sign=0
	for temp_pwd in session.query(pwd).filter_by(where=temp_where).all():
		sign=sign+1
		session.delete(temp_pwd)
	if sign==0:
		print "no this record! delete failed!"	
	else:
		print "delete successful!"	
	session.flush()		
		
def menu():
	print '''************************************************ 
            password keeper 1.0
************************************************ 
   1.Look   2.Add  3.Delete  4.Exit
************************************************ ''' 
def main():
	parser = argparse.ArgumentParser(description='keep password')
	parser.add_argument('-look',help='look the user and pass word now')
	parser.add_argument('-add')
	menu()
	running=True
	while running:
		cmd = raw_input('Input a Command: ')
		if cmd == '1' :
			look()
		elif cmd == '2' :
			add()
		elif cmd == '4' :
			running = False	
		elif cmd == '3' :
			delete()
		else:
			print "Please input a command!"
	print "Thank you for using!"

if __name__=="__main__":
	main()		
