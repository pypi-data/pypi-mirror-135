import re
from .utils.http import Http
from .utils.CONST import HOST


class OpenDataClient:

    def __init__(self, username, password):
        self._username = username
        self._password = password
        Http.login(username=self._username, password=self._password)


    def __getattr__(self, attr):
        if '__' in attr:
            return getattr(self.get, attr)
        return _Callable(self, attr)




class _Executable(object):

    def __init__(self, client, method, path):
        self._client = client
        self._method = method
        self._path = path

    def __call__(self, **kwargs):
        http = Http()
        if self._method == 'GET':
            return http.get(self._parse_url, **kwargs)
        if self._method == 'POST': 
            return http.post(self._parse_url, **kwargs)
        

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)


    @property
    def _parse_url(self):
        url = re.sub('[A-Z]+', lambda x: '/' + x.group().lower(), self._path)
        return HOST + url

    __repr__ = __str__


class _Callable(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'get':
            return _Executable(self._client, 'GET', self._name)
        if attr == 'post':
            return _Executable(self._client, 'POST', self._name)
        name = '%s/%s' % (self._name, attr)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__