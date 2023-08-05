# 简答开放数据 
 - wukehao@jddatatech.com。


## Requirements

python >= 3

## Install
```
python -m pip install jdodata
```


## Usage

```
# login
from jdodata import OpenDataClient
client = OpenDataClient(username="test", password="test") # Username and password:  contact to wukehao@jddatatech.com pls.
 
params = {
    "fund_code": "510080"
}
 
ret = client.ApiStockpediaFundNet_value.get(params=params)
 
ret = client.ApiFund_assistantFundNet_value.get(params={"fund_code": "510080"})
```