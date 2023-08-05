简答数据开放数据
================

-  用户名密码申请请联系 wukehao@jddatatech.com。

环境要求
--------

python >= 3

安装
----

::

    python -m pip install jdodata

使用
----

::

    # 登陆
    from jdodata import OpenDataClient
    client = OpenDataClient(username="test", password="test") # 账号密码请联系 wukehao@jddatatech.com 索取.
     
    params = {
        "fund_code": "510080"
    }
     
    ret = client.ApiStockpediaFundNet_value.get(params=params)
     
    ret = client.ApiFund_assistantFundNet_value.get(params={"fund_code": "510080"})
