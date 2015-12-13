# Senthor
## - A Sentimental Analysis Tool for News Comments

#新闻评论情感分析系统

---

##模块
* 守护进程Daemon模块
* Web服务器模块
* 前端查询与可视化模块
* 文本情感分析模块
* 爬虫模块
* 推荐模块(Optional)

##以下详细介绍各个模块的详细内容，请大家详细补完各自模块的 *实现方法和接口* ，方便最后组装

####守护进程

#####功能介绍：  
守护进程一旦开启就常驻后台。  
1.启动WebServer使得用户能够通过浏览器发起请求和显示结果  
2.定时调用爬虫模块，爬取新闻后存储在文件中，之后返回调用情感分析模块，对于每条新爬取的新闻的评论内容进行情感分析，得到结果也存储起来。  
3.对于前端发来的新闻关键词请求，在文件(或DB)中进行关键词搜索，如果搜索失败就返回ERRCODE，否则就返回所有的匹配新闻的情感关系  
#####分工：
杨子岳、刘家霖(暂定)
#####实现方式：
**(等待填写)**

---
####Web服务器模块

#####功能介绍：
Web服务器由Daemon启动，之后也一直常驻后台。服务器在利用本地某个端口提供用户交互页面，在该页面提供查询接口。
#####分工：
刘家霖(暂定)
#####实现方式：
* 目前我实现了Naive Web Server。
	* 目前的情况是只实现了GET Method，支持基本的js和html自然是没问题，但是对于POST方法无能为力(我还不会实现POST，somebody能实现POST的可以接着陪我造轮子，基于Python的socket包理论上应该不难)
	* 目前JSON RPC模块需要POST方法，所以考虑暂时使用下面的方案
* Apache方案
	* 本来我也考虑过吴鹏说的架设一个Django或者Tornado这些Python版本服务器，后来我发现没有这个必要，因为我的DigitalOcean服务器和杨子岳的Aliyun服务器和我本机上(Mac自带的)都有Apache服务器所以就没有必要再搬运一个轮子了。
	* 如果可以的话我们可以回头再改我的NaiveServer2333
**(等待填写)**

---
####前端查询与可视化模块

#####功能介绍：
前端页面由给用户提供一个良好接口，方便用户查询。用户发起查询后，将请求直接传给守护进程，守护进程执行既定程序逻辑后返回结果给前端。  
**结果分两种：**  
1. 当无法查询到时，(当前版本)返回错误信息直接返还给用户。  
2. 否则，调用可视化模块，利用返回的数据实现图表绘制呈献给用户。  

#####分工：
刘家霖、李芊(暂定)
#####实现方式：
* 语言基础:Javascript(PHP) 
	* 由于这次我们只需要一个主页，只要能有良好的JSON RPC接口的语言使用就可以了。 
* 前端可视化模块：D3.js
	* 谁有兴趣来弄一下都可以，大家都没用过这个可视化工具。不过基于Javascript的可视化包很多，如果D3不行的的话我们可以试试别的。这个还是很重要的，其他模块在展示的时候其实可以随便糊弄，这个就是我们项目的脸，脸好了分绝不会低的。(以上都是我瞎编的) (其实我可以去试试，反正都没学过而且这个模块相对独立，我还有学长帮助233 但是到时候自打脸不要打我就好- by芊)

---
####文本情感分析模块
#####功能介绍：
对于每条新闻的每条评论文本，该模块作为输入得到一个[-1, 1]之间的实数值。
###**问题：最后如何整合各条情感分析的值？(需要补全)**
#####分工：
吴鹏、李芊(暂定)
#####实现方式：
* **textblob(目前暂定)**
	* 由于昨天吴鹏所说的pythonAPI我们都觉得非常方便，所以暂时定为这个工具。但是它的相对效果目前未知，我们在之后可以尝试其他的工具。
* Sentiment Analysis API: http://www.alchemyapi.com/products/alchemylanguage/sentiment-analysis
* Sentiment Analysis in Colombian Online Newspaper Comments: http://link.springer.com/chapter/10.1007%2F978-3-642-28798-5_16


---

####爬虫模块
#####功能介绍：
由Daemon调用，定时爬取选取好的网站的新闻以及评论。(可以试着对每条新闻摘取几个关键词。) (我觉得可以看看有没有发现热点新闻的API，然后返回得到关键词再爬 -by 芊)
以文件的形式保存在本地，并通知Daemon来进行下一步流程。
#####分工：
杨子岳、吴鹏、李芊、刘家霖(**我个人觉得这个任务其实不轻松，所以把大家的名字都挂上去，如果杨大神遇到了麻烦大家就救救他XD**)
#####实现方式：
* Scrapy
	* 这是Python下的很强大的工具。大家如果不了解的话我在这里挂个官方Documentation的[链接](https://media.readthedocs.org/pdf/scrapy/1.0/scrapy.pdf)
* Selenium
	* 所向披靡的网页测试工具,用它挂上chrome来做爬虫虽然慢了点但是chrome有多强我们的爬虫就能有多强(

#####各爬虫模块说明

####crawler_yahoo(2015.12.4 updated by yzy): 
针对雅虎新闻网（news.yahoo.com）的爬虫，抓取四个分类（US, WORLD, TECH, SCIENCE），xpath一波流
#####依赖
* scrapy

#####用法
	cd crawler/crawler_yahoo
	scrapy crawl crawler_yahoo > out.txt

#####输出说明
每一行是一个JSON格式的新闻，一个新闻包含title, link, article, comments四种属性。
title是新闻标题；
link是新闻链接；
article是新闻内容；
comments是新闻评论。
title, link和article的value是字符串，comments的value是一个array，该array中以字符串作为元素，每个字符串是一条评论。
评论的排列顺序是从时间倒序（即新鲜评论在前面）。

#####注意事项
* 英文雅虎的访问不够稳定，现在这个爬虫可能会漏掉一些新闻
* 现在抓取时用的UserAgent是WP8（Lumia 520）以追求处理简单，如果哪天雅虎把这种网页下架了那这个爬虫就不能用了


####crawler_fox(2015.12.13 updated by yzy): 
针对福克斯新闻网（www.foxnews.com）的爬虫，抓取四个分类（US, WORLD, TECH, SCIENCE），用selenium配合scrapy实现抓取动态页面内容
抓取评论时会召唤chrome,因此目前可能只能在图形界面下运行,等我电脑回来了再测试改进一下
#####依赖
* scrapy
* selenium
* chrome
* chromedriver: https://sites.google.com/a/chromium.org/chromedriver/home

#####用法
	cd crawler/crawler_fox
	scrapy crawl crawler_fox > out.txt

#####输出说明
同雅虎新闻

#####注意事项
* foxnews的访问速度及其坑爹,因此现在超时时间设置较长(不然动态内容还没加载出来就停止加载了)
* 找了小半年愣是没发现能像雅虎静态爬起来那么舒服的新闻网站...不过动态抓取的话selenium是通用手段




