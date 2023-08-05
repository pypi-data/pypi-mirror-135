import requests
import urllib.parse
from .user import login, logout


class NeedLoginException(Exception):
    pass

class LoginExpireException(Exception):
    pass

class NetworkErrorException(Exception):
    pass

class FailResponseException(Exception):
    pass


class Http:
    jwt = ""
    
    def __init__(self):
        pass
    
    @classmethod
    def login(cls, username, password):
        cls.jwt = login(username=username, password=password)

    @classmethod
    def logout(cls):
        logout(cls.jwt)
        cls.jwt = ''


    def get(self, url, params):
        return self.request('{}?{}'.format(url, urllib.parse.urlencode(params)))


    def post(self, url, payload):
        return self.request(url, payload=payload)


    def request(self, url, payload=None):


        if not self.jwt:
            raise NeedLoginException("需要登陆。")

        headers = {
            'Authorization': 'jwt {}'.format(self.jwt),
        }

        if not payload:
            payload = {}

        req = requests.request("GET", url, headers=headers, data=payload)

        if req.status_code > 500:
            raise NetworkErrorException("网络错误：{}".format(req.status_code))

        if req.status_code == 401:
            raise LoginExpireException("登陆过期：{}".format(req.status_code))

        if req.status_code != 200:
            raise Exception("未知错误：{}".format(req.status_code))

        data = req.json()

        if data['status'] != 'SUCCESS':
            raise FailResponseException("返回失败：{} {}".format(data['status'], data.get("msg", "NONE MESSAGE.")))

        if 'data' in data: return data['data']
        
        if 'status' in data: del data['status']

        if 'msg' in data: del data['msg']

        if 'message' in data: del data['message']

        return data


