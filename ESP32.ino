#include <WiFi.h>
#include <PubSubClient.h>
//导入必要的库

//下面是定义需要用到的变量，根据实际情况来修改
//######################################################################################

// 我这里读取的是传感器的电压值，所有定义模拟电压
const int analogInPin = 32; // 对A0口赋值
float sensorValue = 0;       // 初始定义模拟值

//######################################################################################

//下面定义的是卡尔曼滤波的相关数值

float x_est = 0;      // 估计的状态
float P = 1;          // 估计误差的协方差
float Q = 0.001;      // 系统噪声协方差
float R = 0.1;        // 测量噪声协方差

//#######################################################################################

// 定义WiFi连接的相关变量，下面是我的热点，请不要蹭谢谢

//#######################################################################################

// MQTT发布消息

//我们这里使用公用的代理服务器，因为是公用的，所以请把你的主题名字起的尽量尽量复杂，这样就不会因为重名接收到别人的消息
const char *mqtt_broker = "broker.emqx.io";//如果你部署了自己的服务器，请把这里改成自己的地址

const char *topic = "esp32/test/kangfupinggu";//这个就是发布的主题名称，一定要记住，因为订阅的时候要根据主题来接受消息

const char *mqtt_username = "";//因为使用的是公共免费的代理服务器，所以没有限制设备的接入
const char *mqtt_password = "";//如果你使用了自己部署的服务器，也可以自己去设置设备的权限，那么就要在这输入自己的设备名和自己设定的密码
const int mqtt_port = 1883;//mqtt协议通用端口号1883

//#######################################################################################

WiFiClient espClient;
PubSubClient client(espClient);

//当我们使用ESP32连接到WiFi网络时，我们需要一个用于与WiFi通信的客户端。WiFiClient就是这样一个客户端，它帮助我们与WiFi建立连接并进行数据传输。
//另一方面，当我们使用MQTT协议与MQTT代理服务器进行通信时，我们同样需要一个客户端。PubSubClient是一个专门用于MQTT通信的客户端库，它帮助我们连接到MQTT代理服务器，并发送和接收MQTT消息。
//在代码中，通过创建一个espClient对象，并将其作为参数传递给PubSubClient构造函数，我们将WiFi客户端和MQTT客户端结合在一起。这样，我们就可以使用同一个客户端对象来处理WiFi和MQTT通信，简化了代码的编写和管理。

//#######################################################################################

int counter = 1; // 初始化计数器

//#######################################################################################
//好，下面是配置函数，基本不用改

void setup() {
  // 设置软件串行波特率为115200
  Serial.begin(115200);

  // 连接到WiFi网络
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to the WiFi network");

  // 连接到MQTT代理
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += WiFi.macAddress();
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Public EMQX MQTT broker connected");
    } else {
      Serial.print("Failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }

  // 订阅主题
  client.subscribe(topic);
}

//#######################################################################################
//到这里


void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

//这一块实际上用处不大，这是一个回调函数，我们这个项目是上传数据的，有兴趣可以了解一下
//topic：一个指向字符数组的指针，表示接收到消息的主题名称。
//payload：一个指向字节数组的指针，表示接收到的消息内容。
//length：一个无符号整数，表示接收到的消息内容的长度。
//#######################################################################################

void loop() {
  client.loop();
  //卡尔曼滤波部分可以略过
//####################################################################################### 
  // 读取模拟电压
  sensorValue = analogRead(analogInPin);

  // 卡尔曼滤波
  float K = P / (P + R);
  x_est = x_est + K * (sensorValue - x_est);
  P = (1 - K) * P + Q;

  Serial.print("sensor = ");
  Serial.println(sensorValue); // 串口打印原始模拟值
  Serial.print("Filtered V = ");
  Serial.println(x_est); // 串口打印滤波后的值
  //到这里
//#######################################################################################
  // MQTT发布
  String payload = String(x_est, 2);
  client.publish(topic, payload.c_str());
  
  //这两行代码什么意思呢，简单来说就是String(x_est, 2)是将变量 x_est 转换为一个字符串，并指定精确到小数点后两位的格式。这里的数字 2 表示保留的小数位数。
  //例如，如果 x_est 的值为 3.1415926535，那么 String(x_est, 2) 将返回字符串 "3.14"。
  //通过将浮点数转换为字符串，并指定精确度，你可以将其用作要发布的消息内容。在这种情况下，payload 变量将包含一个带有两位小数的字符串表示的 x_est 值。然后，使用 client.publish() 函数将该字符串发布到指定的主题。
  //如果你想一次发送大量数据，在字符串使用json格式数据就好啦，在后端解析一下就好，不是很难的
  delay(200); // 延时0.2秒再次读取，也可以更短或者更长，看个人需求

}

//快去试试吧