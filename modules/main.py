#coding=utf-8

from sqlalchemy.orm import Session
import create_schema

def main():
    session = Session(bind=engine)
