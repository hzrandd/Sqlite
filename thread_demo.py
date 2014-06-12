#-*-coding:utf-8-*-

'''author: ruandongdong
   email: ruandongdong2012@gmail.com
'''

import threading
import os
import sqlite3


def conn_trans(func):
    '''
    数据库连接相关的拦截器.在func调用前连接数据库,func调用结束提高事务并关闭连接.
    '''
    def connection(self, *args, **kwargs):
        self.lock.acquire()
        conn = self.get_conn()
        kwargs['conn'] = conn
        rs = func(self, *args, **kwargs)
        self.conn_close(conn)
        self.lock.release()
        return rs
    return connection


class Dao(object):
    '''
    数据持久化处理类
    '''

    def __init__(self, path, name='', *args, **kwargs):
        '''
        初始化工作...
        '''
        self.lock = threading.RLock()
        self.name = name
        self.path = path
        db_path = self.path[:self.path.rfind(os.sep)]
        if os.path.exists(db_path):
            os.makedirs(db_path)

    def get_conn(self):
        '''
        建立连接，为什么不能设置为实例成员？自己想想，－－
        '''
        conn = sqlite3.connect(self.path)
        return conn

    def conn_close(self, conn=None):
        '''
        操作完，关掉连接
        '''
        conn.close()

    def save(self, obj, conn=None):
        '''
        保存数据
        '''
        cu = conn.cursor()
        cu.execute(obj.to_insert_sql())

    @conn_trans
    def safe_save(self, obj, conn=None):
        '''
        保存数据
        '''
        cu = conn.cursor()
        cu.execute(obj.to_insert_sql())
