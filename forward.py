# 首先我们先来了解一个概念
# 什么是脚本
# 脚本，顾名思义是使用一种特定的描述性语言，依据一定的格式编写的可执行文件，又称作宏或批处理文件。 脚本通常可以由应用程序临时调用并执行。 通俗来讲，脚本语言就是解释执行的语言。
# 那么说人话，脚本就是遗传能够一直运行的代码，能够不断的处理特定的任务
#
# 在我们前面的步骤中，我们已经可以用ESP32把数据上传至特定的主题，那么主题的消息该怎么存入我们的数据库中呢，我们需要一串一直运行的代码，也就是脚本，我们需要一直订阅主题发送的消息，然后把消息是插入数据库中。
# 下面，让我们一起来看看用python写的简单脚本吧

#那么，首先可以看到我们引用了这么多库，那么他们都有什么用呢

import logging
import time
import mysql.connector
import paho.mqtt.client as mqtt
import mysql

# logging：Python 标准库中的一个模块，提供了记录日志的功能。在程序开发和调试过程中，可以使用该模块来输出各种信息以及错误、警告等级别的日志消息。
# time：Python 标准库中的一个模块，提供了与时间相关的函数。例如，获取当前时间、暂停程序执行、计算时间差等。
# mysql.connector： 一个Python的第三方库，用于连接和操作MySQL数据库。它提供了一组类和方法，使得Python程序可以轻松地连接到MySQL数据库，并执行查询、插入、更新和删除数据等操作。
# paho.mqtt.client： 一个MQTT客户端库，用于与MQTT代理进行通信。它提供了一组类和方法，使得Python程序可以轻松地订阅和发布MQTT主题，以及处理接收到的消息。

#下面的配置信息基本上就不用修改
#可以直接用

# 配置日志
logging.basicConfig(level=logging.INFO)
# 配置MQTT连接
mqtt_broker = "broker.emqx.io"
#这个地方写我们的代理服务器地址
#如果你在前面的步骤中部署了自己的代理服务器
#在这个地方更换即可

mqtt_port = 1883
#端口号

mqtt_topic = "esp32/test/kangfupinggu"
#这个地方是我们订阅的主题名称
#要和前面保持一致

mqtt_client_id = "mqtt_data_receiver"
#这里是我们设备的连接名称，可以自己起名字

# 配置MySQL连接
db_host = "121.36.103.123"
db_user = "root"
db_password = "123456"
db_database = "mqtt_data"
#这里配置数据库的连接
#分别是数据库所在的IP地址，登录数据库所用的用户名，用户密码以及访问数据库的名称

# 最大尝试次数
max_retries = 5

# 处理MQTT消息的回调函数

# 首先，将接收到的消息内容解码为字符串，然后连接到 MySQL 数据库，并创建数据库游标。接着将消息存储到数据库中，最后提交更改并关闭连接。在整个过程中，如果出现异常，就将异常信息记录下来，并关闭游标和数据库连接。

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        logging.info(f"Received MQTT message on topic {message.topic}: {payload}")

        # 连接到MySQL数据库
        #这里根据自己数据库表中消息自行修改

        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
        logging.info("Connected to MySQL database.")

        # 创建数据库游标
        cursor = db_connection.cursor()

        # 将消息存储到数据库
        insert_query = "UPDATE table_1 (topic, payload) VALUES (%s, %s)"
        insert_data = (message.topic, payload)
        cursor.execute(insert_query, insert_data)

        # 提交更改并关闭连接
        db_connection.commit()

        logging.info("Message inserted into the database.")

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        cursor.close()
        db_connection.close()

# 接下来是 MQTT 客户端的初始化和连接：
# 首先创建了一个 MQTT 客户端实例，然后将之前定义的回调函数 on_message() 设置到客户端上。接着使用 connect() 方法连接到 MQTT 代理服务器，如果连接成功，则输出日志信息；否则输出错误信息。然后使用 subscribe() 方法订阅 MQTT 主题。

# 创建MQTT客户端
client = mqtt.Client(client_id=mqtt_client_id)
client.on_message = on_message

# 启动 MQTT 客户端的循环，并尝试连接到 MySQL 数据库：
try:
    client.connect(mqtt_broker, mqtt_port)
    logging.info("Connected to MQTT broker.")
except ConnectionRefusedError:
    logging.error("Failed to connect to MQTT broker. Check broker settings.")

client.subscribe(mqtt_topic)

# 启动MQTT客户端循环
client.loop_start()

# 尝试连接到数据库
retry_count = 0
db_connected = False

while not db_connected and retry_count < max_retries:
    try:
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
        logging.info("Connected to MySQL database.")
        db_connected = True
    except Exception as e:
        retry_count += 1
        logging.error(f"Error connecting to the database: {e}")
        time.sleep(5)  # 等待一段时间后重试

if db_connected:
    while True:
        pass
else:
    logging.error("Failed to connect to the database after multiple retries. Exiting.")
    client.disconnect()
    client.loop_stop()

# 使用 loop_start() 启动 MQTT 客户端的消息循环。然后使用一个循环，尝试连接到 MySQL 数据库。如果连接成功，则进入一个空循环；否则输出错误信息，断开 MQTT 连接并停止消息循环。

# 这就是脚本的全部内容
# 正确启动的话会显示两行连接信息
# 然后数据库实时存入消息