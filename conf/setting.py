#!/usr/bin/env python
#coding=utf-8

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root:sp880922@localhost/class_management', echo=True)

connection = print('connected to db\n', '-'*10)
