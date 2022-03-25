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
## 概况
- 实际抓取到的数据数：1604551 （用户不存在或等级为0）
- 用户 uid 范围 (1 - 2500128)
- 抓取字段： 用户uid，用户名，性别，等级，是否处于封禁状态，曾经拥有大会员状态，是否拥有直播间，学校信息，关注数，粉丝数，获赞数，总视频播放数，充电人数 
