<!--
 * @Author: 饕餮
 * @Date: 2022-01-21 10:36:35
 * @version: 
 * @LastEditors: 饕餮
 * @LastEditTime: 2022-01-21 15:38:34
 * @Description: README
-->
# Hunter-SDK
奇安信 Hunter SDK

## Quick Start

### 访问Hunter官网注册账号
https://hunter.qianxin.com/

### 安装SDK
```
pip3 install hunter-sdk
```

### 构建配置文件

config.json
```json
{
    "Hunter":{
        "username":"your name",
        "apikey":"xxxxx"
    }
}
```

### 开始使用
```python
from hunter_sdk.Hunter import Hunter
# 第一个参数是配置文件，第二个参数是存储信息的key
hunter = Hunter('config.json','Hunter')
# 正常查询
rep = hunter.Search("ip=180.97.168.79")
print("Page Total:{}".format(hunter.TotalPage))
print("Now Page:{}".format(hunter.NowPage))
print("IP List:")
for t in rep.HunterList:
    print("{}:{}".format(t.Ip,t.Port))
time.sleep(2)
print("----------------------------")
# 下一页(必须查询过一次才可以操作)
rep = hunter.Next()
print("Page Total:{}".format(hunter.TotalPage))
print("Now Page:{}".format(hunter.NowPage))
print("IP List:")
for t in rep.HunterList:
    print("{}:{}".format(t.Ip,t.Port))
time.sleep(2)
print("----------------------------")
rep = hunter.Next(99)
print("Page Total:{}".format(hunter.TotalPage))
print("Now Page:{}".format(hunter.NowPage))
print("IP List:")
for t in rep.HunterList:
    print("{}:{}".format(t.Ip,t.Port))

```

## 说明
此版本后续可能会更新，用于生产环境，请注意版本说明