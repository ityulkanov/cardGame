import requests
import threading
import time
import config

class Client:
    def __init__(self):
        self._url = config.HOST
        self._login = None
        self._state = None
        self._pool = ClientPoolThread(self)

    @property
    def login(self):
        if self._login is not None:
            return self._login
        else:
            return 'not log on yet'

    def api_method(method):
        def dec(f):
            def wrap(*args,**kwargs):
                self = args[0]
                resp = requests.post(self._url + method, json={'login':self.login})
                if resp.status_code != 200:
                    raise ClientError(resp.json()['status'])
                else:                    
                    return f(*args,resp,**kwargs)
            return wrap
        return dec

    def log_in(self, login, resp=None):
        resp = requests.post(self._url + 'login', json={'login':login})
        if resp.status_code != 200:
            raise ClientError(resp.json()['status'])
        else:
            self._login = login
            return resp.json()['status']

    @api_method('create-game')
    def create_game(self,resp):
        self.start_pooling()
        return resp.json()['status']

    @api_method('join-game')
    def join_game(self,resp):
        self.start_pooling()
        return resp.json()['status']

    @api_method('ready')
    def ready(self,resp):
        return resp.json()['status']
    @api_method('call')
    def call(self, resp):
		return res.json()['status']

    @api_method('rising')
    def rising(self, resp):
    	return res.json()['status']

    @api_method('all-in')
    	return res.json()['status']
    @api_method('check')
    	return res.json()['status']

    @api_method('all')
    def start_pooling(self):
        if self._state is None:
            self._pool.start()

    def stop_pooling(self):
        self._pool.stop_pool()
        self._pool.join()

    def call('')


class ClientPoolThread(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self._client = client
        self.pooling = True

    def run(self):
        i = 1
        while self.pooling:
            #Fake request
            self._client._state = 'WORK {0}'.format(i)
            i += 1
            time.sleep(1)

    def stop_pool(self):
        self.pooling = False


class ClientError(Exception):
    def __init__(self,message):
        super().__init__(message)

        self.message = message
