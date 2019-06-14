# weiboSpider
用python爬取新浪微博和评论数据（闲得无聊写的，没仔细调试…）

## 前言
本人长这么大第一次深入饭圈追星，逐渐了解了饭圈所谓的“做数据”后，对大量的评论转发比较好奇，所以尝试写了一个爬虫抓取的code。具体参考了如下两个链接（原始code并没有发布在github上，无法fork）

* [Python抓取微博评论](https://www.cnblogs.com/chenyang920/p/7205597.html)
* [python爬虫抓取新浪微博数据](https://www.jianshu.com/p/c4ef31a0ea8c)

私心放一张妹妹照片！！！我妹妹真的超级好！！！希望大家有机会可以了解一下！！！入股不亏！！！
![Image of Meiqi Meng](./images/meiqi.JPG)

## 数据加载

首先，整个程序是通过模拟手机端访问http://m.weibo.com 来请求数据的，因此首先要找到要访问的主页的网址。以火箭少女101官博为例，
```
def get_user_info(page):
    params = [
        ('type', 'uid'),
        ('value', 6576856192),
        ('containerid', 1076036576856192),
        ('page', page)
    ]
```
### 用户
可以看到，每一个用户都有指定的ID，在程序中只要替换params的value和containerid即可访问相应的用户。
![官博网址](./images/rocketgirls.png)

### 微博
在chrome的development tool功能下可捕捉到如图所示的请求。

![RequestURL](./images/details.png)


图片里高亮的Link即为Request URL，里面包含了该微博用户目前发表前10条微博的所有信息（如果需要抓取更多微博，调整params里的变量page即可，默认0）。Jason数据结构如下图所示

![Structure](./images/structure.png)


### 评论
目前微博的评论有两种排序方式，一个是时间，一个是热度（热度的排序机理我不是很了解，目前知道的情况是，点赞越多排的越高？？），而网页版微博默认显示热度排序，及hotflow。在chrome的development tool功能下可捕捉到如图所示的请求。
```
getIndex?type=uid&value=6576856192&containerid=1076036576856192
```
图片里高亮的Link即为Request URL，里面包含了这个

![最新微博](./images/details.png)
