import os
import re
import json
import pandas as pd
import psycopg2

class Postgres:
    def __init__(self, **kwargs):
        self._exception = None
        self._server = kwargs.get('server')
        self._user = kwargs.get('user')
        self._passwd = kwargs.get('passwd')
        self._port = kwargs.get('port')
        self._db = kwargs.get('database')
        if kwargs.get('timeout') is None:
            self._timeout = 60
        else:
            self._timeout = kwargs.get('timeout')
        self._connect()
        
    # Set exception
    def _set_exception(self,value):
        self._exception = value  
        
    def exception_msg(self):
        msg = None
        if str(self._exception).find('authentication failed')!=-1:
            msg = 'ERROR: '+self._user+' password is wrong'
        elif str(self._exception).find('timed out')!=-1:
            msg = 'ERROR: timed out, server not reachable'
        elif self._exception is not None:
            msg = 'ERROR: '+str(self._exception)             
        return msg

    def _connect(self):   

        try:
            self._connection = psycopg2.connect(
                host=self._server,
                user=self._user,
                password=self._passwd,
                connect_timeout=self._timeout,
                port=self._port,
                database=self._db
            )
        except Exception as e:
            self._set_exception(e)
    
    # Close the DB connection   
    def close(self):
        try:
            self._connection.close()
        except:
            pass
             
    # Run the SQL
    def _run_sql(self,statement):
            
        # Run only if there wasn't any error before
        if self._exception is None:
            
            try:
                self._cursor = self._connection.cursor()
                self._cursor.execute(statement)
            except Exception as e:
                self._set_exception(e)  

    def get_records(self,statement):
        self._run_sql(statement)
        if self._exception is None:
            try:    
                return self._cursor.fetchall()
            except Exception as e:
                self._set_exception(e)
        else:
            return -1
    

class File():
    '''
    Provide full path for file on local 
    '''
    def __init__(self,filepath):
        self.filepath=filepath

    #self._exception = None

    def _set_exception(self,value):
        self._exception = value
        
    def exception_msg(self):
        msg = None
        if self._exception is not None:
            msg = 'ERROR: '+str(self._exception) 
        return msg

    def get_season(self):
        reg = re.compile('[E]{1}[0-9]{4}')
        self.season = str(reg.findall(self.filepath)[0][-4:])
        return int(self.season)

    def get_content(self):
        try:
            with open (self.filepath) as f:
                self.content = json.loads(f.read())
        except Exception as e:
            self._set_exception(e)
        return self.content
    
    # def get_content_df(self):
    #     try:
    #         self.df = pd.DataFrame(self.get_content()['Rows'])
    #     except Exception as e:
    #         self._set_exception(e)
    #         print(e)
    #     return self.df        


class Folder():  
    '''
    Provide root directory on your local where you store the data
    '''
    def __init__(self,rootdir):
        self.rootdir=rootdir
    
    def get_subdirs(self):
        self.subdirs = [x for x in os.walk(self.rootdir)]
        return self.subdirs


class Lib():
    '''
    input
    cols : list with column names
    '''
    @staticmethod
    def create_empty_dataframe(cols):
        df = pd.DataFrame(columns=cols)
        return df


    





