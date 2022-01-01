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

## API

****

#### 获取所有视频信息

***getVideos***

api/v1/videos/{page}/info get

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|page|Int|false|1|页码|
|page_size|Int|true|1|每页容量|

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
      "firstEp": 1000
    }
  ]
}
```

#### 获取单个视频信息

***getVideo***

api/v1/video/{vid} get

#### Request

|名字|类型|可选|举例|说明|
|---|---|---|---|---|
|vid|Int|false|10000|video的主键id|

#### Response

```json
{
  "code": 200,
  "msg": "success",
  "episodes": 0,
  "data": {
    "src": "/anime/death_note/death_note01.mp4",
    "img": "/anime/death_note/death_note01.png",
    "episodes": [
      "death_note01.mp4",
      "death_note02.mp4"
    ]
  }
}
```

#### 获取单个视频信息并按type分类

***getVideo***

api/v1/video/{vid}/byClassify get

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
        "src": "http://127.0.0.1:9000/46080260$$哈尔的移动城堡/tv/3038794862$$移动城堡.mp4",
        "id": 3038794862,
        "name": "移动城堡"
      },
      {
        "type": "tv",
        "src": "http://127.0.0.1:9000/46080260$$哈尔的移动城堡/tv/8706999328$$移动城堡 (2).mp4",
        "id": 8706999328,
        "name": "移动城堡 (2)"
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

#### 更新数据库中本地资源的数据

***updateLocal***

local/synchronize post

#### Request

```json
{
  "title": [
    "air",
    "clannad"
  ]
}
```

#### Response

```json
{
  "code": 200,
  "msg": "success"
}
```

***其它***

#### Bad responses

```json
{
  "code": 400,
  "msg": "failed"
}


```
