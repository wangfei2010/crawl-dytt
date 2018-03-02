# -*- coding : utf-8 -*-
from pymongo import MongoClient

class MongodbUtils:
    __conn = None
    db = None

    def __init__(self):
        self.__conn = MongoClient('localhost', 27017)

    def __closeDb(self):
        self.__conn.close()

    def __getCollection(self):
        db = self.__conn.test
        return db.stu

    def add(self, obj):
        self.__getCollection().insert(obj)
        self.__closeDb()

    def save(self, obj):
        self.__getCollection().save(obj)
        self.__closeDb();

    def saveAll(self, arr):
        for obj in arr:
            self.__getCollection().save(obj)
        self.__closeDb()

    def update(self, obj):
        self.__getCollection().update(obj)
        self.__closeDb();

    def get(self, obj):
        data = self.__getCollection().find(obj)
        self.__closeDb()
        return data

    def getOne(self, obj):
        data = self.__getCollection().find_one(obj);
        self.__closeDb()
        return data
