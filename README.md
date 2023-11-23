# ESP32 数据上云
主要讲述如何使用EMQX订阅主题来打通项目中的数据流


我会给出相关的网站教程以及相关的代码
代码使用康复评估项目的代码示例
这里将使用EMQX公开免费的代理服务器，免费又快速的代理服务器，谁又能不喜欢呢
当然如果你真的喜欢部署自己的代理服务器，好吧朋友
这是教程，也是不难的，部署好之后下面的流程还是一样的
部署代理服务器：https://docs.emqx.com/zh/cloud/latest/create/serverless.html


可以把传感器数据传输至本机电脑或者说服务器上，然后我会给出转发脚本，存入数据库
![image](https://github.com/Innovation-Pulse/data-transmission/assets/144523816/f786e2ba-0def-4e11-9ae7-2c641089bd7a)


不需要很多的专业知识
很简单就可以做到实时传输
传输效果很稳定

当然你需要了解一些MQTT订阅机制的相关知识（不想看可以直接跳过，不影响的，感兴趣就可以多学一些）

#################################################################################################################################

MQTT 是一种轻量级的消息协议，它允许设备之间通过互联网进行通信。在 MQTT 中，消息以主题（Topic）的形式发布和订阅。主题是一个用于标识消息内容的字符串，可以看作是消息的地址。

消息订阅就像是你订阅了一份杂志，在你关注的主题有新消息时，你就会收到最新的内容。在 MQTT 中，客户端可以订阅一个或多个主题，当有新消息发布到对应的主题时，客户端就会收到这个消息。订阅主题可以是精确匹配，也可以使用通配符匹配。

代理机制则是 MQTT 的核心特性之一，它允许消息从一个客户端传递到另一个客户端。代理服务器是一个中继站，它接收来自发布者的消息，并将其转发到订阅者。代理服务器可以将消息缓存起来，以便在发布者和订阅者之间出现网络故障时，消息不会丢失。

总结一下，MQTT 的消息订阅和代理机制就像是订阅了一份杂志并指定了邮寄地址，代理服务器就像是一个邮局，负责按照地址将杂志送到你手中。这种机制简单易懂，但却非常实用，在物联网等应用场景中得到了广泛的应用。

#################################################################################################################################

下面是详细教程（有一些详细的教程放在代码注释进行）：

首先需要打开ESP32的代码，对ESP32进行烧录，当然朋友，如果你想用arduino板或者是esp8266也是可以的，本质上又有什么区别呢？

我会详细注释一下代码的部分

接下来需要下载MQTTX软件，来检测数据是否成功发送主题

软件的下载地址以及超级超级详细的安装教程如下：
https://docs.emqx.com/zh/cloud/latest/connect_to_deployments/mqttx.html

好的，如果你成功看到了MQTTX上跳动的消息，说明你已经成功了80%

那么接下来，就是看我们下一个python文件，当然必要的库还是要装一下的
直接使用PIP或者在pycharm里面安装一下即可，应该没什么难度

好吧我还是写一下（在命令行<win+R然后输入cmd按回车>然后输入下面两行代码来运行

MySQL Connector库用于连接和操作MySQL数据库。
pip install mysql-connector-python

paho-mqtt：用于与MQTT代理进行通信。
pip install paho-mqtt

然后根据我注释的python代码进行修改，即可完成操作

记得下载数据库

我也放一下教程

这篇写的很详细：https://blog.csdn.net/m0_74097410/article/details/131048373?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522170066220716800184162331%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=170066220716800184162331&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-131048373-null-null.142^v96^pc_search_result_base8&utm_term=%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8B%E8%BD%BD%E6%95%99%E7%A8%8B&spm=1018.2226.3001.4187

好，希望能成功，祝好运

