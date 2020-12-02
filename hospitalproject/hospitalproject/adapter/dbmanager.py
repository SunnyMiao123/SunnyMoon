import os
import pymongo.mongo_client as client

class dbmanager:

    def __init__(self):
        super().__init__()
    host='127.0.0.1'
    port=27017
    
    def ConnectDB(self):
        """
        连接数据库
        """
        try:
            mongod = client.MongoClient(host=self.host,port=self.port)
            print(mongod.server_info())
            return mongod
        except :
            raise BaseException()

    def ConnectDB2(self,host,port):
        mongod = client.MongoClient(host=host,port=port)
        return mongod

    def TestDB(self):
        """
        测试连接
        """
        mongod = client.MongoClient('192.168.1.1',27017)
        return mongod

"""
if __name__ == "__main__":
    db = dbmanager()
    print(db.ConnectDB())
    print(db.TestDB())
"""