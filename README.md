# BiliBili-User-Analysis
Get bilibili user info using python

Used ip pool for proxies (20000+ ips), random user-agent, random referer, random timeout to bypass the ip ban

Used concurrent requests to increase efficiency

Timeout setting should remain unchanged, lower timeout setting is not recommanded
#
**该爬虫仅供学习使用**


API信息及参数皆取自 https://github.com/SocialSisterYi/bilibili-API-collect

# 基本信息分析
出于成本考虑我只抓取了大概前250万用户（uid <= 2500128）， 如果你时间充裕可以用少一些的ip数量以及延长request间隔来抓取所有用户信息。（最大uid可以用 binary search 找出）

前250万用户说明这些用户都是元老级的b站用户，他们的统计数据肯定是有很大的bias的不能用作整体分析， 主要就是图一乐。
## 概况
- 实际抓取到的数据数：1604551 （用户不存在或等级为0不计入）
- 用户 uid 范围 (1 - 2500128)
- 抓取字段： 用户uid，用户名，性别，等级，是否处于封禁状态，大会员状态，是否拥有直播间，学校信息，关注数，粉丝数，获赞数，总视频播放数，充电人数 

## 性别

- 男： 119307
- 女： 5943
- 保密：1421021

![image](https://user-images.githubusercontent.com/50432664/160083363-d84576f5-05f1-4e0b-9b8f-334389ed3ed3.png)

大部分用户都选择了隐藏性别，没有隐藏的用户男女比例差异还是有点大的

## 等级

- lv 6: 405843
- lv 5: 619348
- lv 4: 181272
- lv 3: 112672
- lv 2: 113685
- lv 1: 171731

![image](https://user-images.githubusercontent.com/50432664/160084051-8a748489-2ee8-4ff7-81e0-ea8d273168ef.png)

早年间加入B站的现在大多都已经是5，6级了

## 封禁状态

- 封禁人数: 10241
- 占比： 6.38%

- lv 6: 886
- lv 5: 2933
- lv 4: 1491
- lv 3: 2429
- lv 2: 1165
- lv 1: 1337

![image](https://user-images.githubusercontent.com/50432664/160085832-80d8829c-da04-43d5-9b1e-7fd7c51c0f50.png)

仁者见仁智者见智

## 大会员状态
- 至少拥有过年大会员：559984
- 至少拥有过月大会员：447517
- 从来没拥有过大会员：597050

![image](https://user-images.githubusercontent.com/50432664/160087245-e187c94f-2a38-44c6-9afa-96a67c20b1c5.png)

老用户粘性还是不错的，给叔叔充过钱的比例不低

## 直播间状态
- 有直播间：778056
- 没有直播间：826495

![image](https://user-images.githubusercontent.com/50432664/160087836-21b654e5-8ec5-4654-831f-4421036d36ad.png)

开通直播间需要手持身份证验证，还挺麻烦所以有直播间的多多少少对做主播有点兴趣吧

## 学校信息
我先把做这个项目之前的猜测放在这里：都不用看就知道清华北大肯定是最多的，至于原因嘛懂得都懂。 结果也是不那么意外虽然第二不是但也很接近。我把Top 20 列出来

- 有效数据：25873
- 清华大学： 606
- 上海交通大学：566
- 北京大学：534
- 浙江大学：466
- 复旦大学：417
- 华中科技大学：322
- 武汉大学：312
- 同济大学：296
- 电子科技大学: 289
- 中山大学: 286
- 四川大学: 269
- 南京大学: 238
- 哈尔滨工业大学: 223
- 厦门大学:	209
- 东南大学:	208
- 吉林大学:	199
- 中南大学:	197
- 华南理工大学:	177
- 北京航空航天大学:	176
- Top 20：5990
- 其他：19883

![image](https://user-images.githubusercontent.com/50432664/160091231-e8cff27b-34cb-49f7-a455-ac8ccc1c963f.png)

## 粉丝数

top 20

![image](https://user-images.githubusercontent.com/50432664/160095675-87c0e97b-78a8-4431-9428-f2e3c81fe8a1.png)

都是老熟人了， 元老用户中老番茄混的最好

## 获赞数

top 10

![image](https://user-images.githubusercontent.com/50432664/160096528-8cbafde7-b2b3-4b1e-bb7e-a07b7cb7b7e5.png)

## 视频播放量

top 20

![image](https://user-images.githubusercontent.com/50432664/160098229-31249efe-9b9c-4801-aa6c-c47447609556.png)

私心推荐老菊的视频，成为未来科技的员工吧！

## 充电人数

top 10

![image](https://user-images.githubusercontent.com/50432664/160098873-390c1eeb-c0b1-4919-abea-65b91a99e1be.png)

个人见解，优质内容+粉丝粘度和充电人数正相关


