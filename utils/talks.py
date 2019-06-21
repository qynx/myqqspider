import json
import datetime
import logging
import pymysql

logger = logging.getLogger("main")

class Talk():

    _id = ""
    _content = ""
    time = ""
    name = ""
    author = ""
    images = []
    insert_time = ""
    li_id = ""

    def __init__(self):
        self.insert_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if value is None or value == []:
            value = ""
        self._content = value


    def insert(self, cursor):
        '''
        @param cursor: pymysql's conn's cursor
        '''
        sql_pattern = 'insert into logs(content, li_id, name, author, time, images, insert_time)\
               values("{content}", "{li_id}", "{name}", "{author}", "{time}", "{images}", "{insert_time}")'
        # import pdb; pdb.set_trace()
        sql = sql_pattern.format(content=pymysql.escape_string(self._content),
                                 li_id=pymysql.escape_string(self.li_id),
                                 insert_time=self.insert_time,
                                 name=pymysql.escape_string(self.name),
                                 author=pymysql.escape_string(self.author),
                                 images=pymysql.escape_string(json.dumps(self.images)),
                                 time=self.time)
        logger.debug(sql)
        cursor.execute(sql)

    