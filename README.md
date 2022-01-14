## yuzuhiVideo

在线观看视频的网站

### 配置文件

## 数据库

****

#### episodes

|id|src|name|type|videoID|position|timestamp|
|---|---|---|---|---|---|---|
|1|http://127.0.0.1/video/clannad/01.mp4|1|tv|5|local|10000|

#### videos

|id|title|img|timestamp|episodes|position|
|---|---|---|---|---|---|
|1|air|http://127.0.0.1/video/air/air.png|10000|24|local|

## API 前端交互

****

### get videos

#### 接口名称

```
[GET] api/v1/videos/{page}/info 
```

使用此方法获取指定页码的videos信息

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|page|Number|false|1|页码|
|ip|String|false|192.168.0.1|ip地址|
|page_size|Number|true|1|每页容量|

#### Response

```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 100,
      "title": "death note",
      "img": "/anime/death_note/preview.png",
      "episodes": 5,
      "firstEp": ""
    }
  ]
}
```

### getVideo

```
[GET] api/v1/video/{vid} 
```

获取单个视频信息

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|eid|Int|false|10000|episode的主键id|

#### Response

```json
{
  "code": 200,
  "msg": "success",
  "episodes": 0,
  "data": {
    "episode": 2,
    "id": 3101520130,
    "position": "local",
    "videoID": 82664514,
    "type": "一期",
    "src": "http://127.0.0.1:9000/82664514$$進撃の巨人/一期/3101520130$$2.mp4",
    "timestamp": 1641969042.2792988
  }
}
```

### get video by classify

```
[GET] api/v1/video/{vid}/byClassify
```

获取单个视频下的所有episode信息并按type分类

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|vid|Int|false|10000|video的主键id|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": [
    [
      {
        "type": "tv",
        "src": "http://127.0.0.1:9000/46080260$$哈尔的移动城堡/tv/3038794862$$1.mp4",
        "id": 3038794862,
        "name": "1"
      },
      {
        "type": "tv",
        "src": "http://127.0.0.1:9000/46080260$$哈尔的移动城堡/tv/8706999328$$2.mp4",
        "id": 8706999328,
        "name": "2"
      }
    ],
    [
      {
        "type": "剧场版",
        "src": "http://127.0.0.1:9000/46080260$$哈尔的移动城堡/剧场版/5701790811$$1.mp4",
        "id": 5701790811,
        "name": "1"
      }
    ]
  ]
}
```

### get video all

```
[GET] api/v1/video/{vid}/all
```

获取单个视频下的所有episode信息

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|vid|Int|false|10000|video的主键id|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "episode": 1,
      "id": 2107509866,
      "type": "一期",
      "src": "http://127.0.0.1:9000/82664514$$進撃の巨人/一期/2107509866$$1.mp4"
    },
    {
      "episode": 2,
      "id": 3101520130,
      "type": "一期",
      "src": "http://127.0.0.1:9000/82664514$$進撃の巨人/一期/3101520130$$2.mp4"
    },
    {
      "episode": 3,
      "id": 5847011366,
      "type": "一期",
      "src": "http://127.0.0.1:9000/82664514$$進撃の巨人/一期/5847011366$$3.mp4"
    }
  ]
}
```

### record

```
[POST] /api/v1/view/record
```

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|vid|Int|false|10000|video的主键id|
|eid|Int|false|10000|episode的主键id|
|src|String|false|http://127.0.0.1:9000/82664514$$進撃の巨人/一期/3101520130$$2.mp4|视频地址|
|timeline|Int|false|100|视频播放进度(秒)|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": null
}
```

## API 管理

****

### clear

```
[GET] /api/admin/clear/local/all 
```

清除所有静态文件夹与资源的vid与eid

### synchronize all

```
[GET] /api/admin/local/synchronize/all 
```

同步所有视频静态资源至数据库

### synchronize auto

```
[GET] /api/admin/local/synchronize/auto
```

自动同步未同步的视频静态资源至数据库，并删除数据库内过期数据

### synchronize clear

```
[GET] /api/admin/local/synchronize/clear
```

删除数据库内过期数据

### synchronize add title

```
[GET] /api/admin/local/synchronize/add/{title}
```

添加指定的静态文件资源至数据库

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|title|String|false|無職転生|静态资源文件夹名|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "title": "tensei",
    "timestamp": 1641972839.7779293,
    "firstEp": "http://127.0.0.1:9000/498881$$tensei/一期/5622708835$$1.mp4",
    "episodes": 4,
    "position": "local",
    "id": 498881,
    "img": "http://127.0.0.1:9000/498881$$tensei/tensei.png"
  }
}
```

### add user

```
[POST] /api/admin/user/add
```

添加一个新用户

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|ip|String|false|127.0.0.1|ip地址|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "ip": "127.0.0.1",
    "is_delete": 0,
    "id": 12
  }
}
```

### extend user

```
[POST] /api/admin/user/extend
```

为一个用户增加一段ip

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|ip|String|false|127.0.0.1|ip地址|
|uid|Int|false|1|user主键id|

#### Response

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "ip": "129.168.0.0,192.168.0.1,127.0.0.10",
    "is_delete": 0,
    "id": 1
  }
}
```