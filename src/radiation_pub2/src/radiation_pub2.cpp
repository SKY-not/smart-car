#include "ros/ros.h" // 统一头文件
#include "std_msgs/Float64MultiArray.h" // 发布的消息类型
#include <vector> // 向量（数组），用于给发布的消息赋值


// 辐射源位置和系数，仅供调试，初赛测试时会改变
// 不保证辐射源位置只有一位小数，也不保证两个辐射源系数相等
// 0 < x_rad < 3.4 
const double x_rad = 2.6;
const double y_rad = -0.2;
const double x_rad2 = 2.6;
const double y_rad2 = -1.54;
const double k = 20;
const double k2 = 10;

// 发布器和订阅器
ros::Subscriber sub;
ros::Publisher pub;

double dist_sqr(double x1,double y1,double x2,double y2){
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2);
}

void meow(const char* str) {
    // 打开文件
    FILE* fp = fopen("debug_radiation_pub2.txt", "a");
    if (fp == NULL) {
        ROS_ERROR("Failed to open debug.txt");
        return;
    }
    // 写入字符串
    fprintf(fp, "%s\n", str);
    // 关闭文件
    fclose(fp);
}

// 回调函数：订阅新的话题并计算辐射强度
void radiation_pub(const boost::shared_ptr<std_msgs::Float64MultiArray const>& msg) {
    // 创建一个存储辐射强度的 vector
    std::vector<double> radiation_data;
    // 在debug.txt中打印一个调试信息
    //meow("Received points data");
    // 遍历输入数组的每一行
    for (size_t i = 0; i < 36; ++i) {
        double x = msg->data[i * 2];     // 获取第 i 行的第 1 个元素 (x 坐标)
        double y = msg->data[i * 2 + 1]; // 获取第 i 行的第 2 个元素 (y 坐标)

        // 计算辐射强度
        double radiation = k / dist_sqr(x, y, x_rad, y_rad) + k2 / dist_sqr(x, y, x_rad2, y_rad2);

        radiation_data.push_back(radiation); // 辐射强度
    }

    // 发布辐射强度数组
    std_msgs::Float64MultiArray radiation_msg;
    radiation_msg.data = radiation_data;
    pub.publish(radiation_msg);
    // 在debug.txt中打印一个调试信息
    //meow("Published radiation data");
    //ROS_INFO("Processed %lu points and published radiation data.", msg->data.size() / 2);
}

int main(int argc, char *argv[])
{
    // 节点初始化
    ros::init(argc,argv,"radiation_pub2");
    // 实例化 ROS 句柄
    ros::NodeHandle nh;
    // 实例化订阅者对象,参数1是话题名(要保证和发布方的话题一致)
    // 参数2是buffer空间大小，参数3是回调函数
    sub = nh.subscribe<std_msgs::Float64MultiArray>("points", 200, radiation_pub);
    // 实例化发布者对象，参数是话题名，buffer大小
    pub = nh.advertise<std_msgs::Float64MultiArray>("radiation2", 20);
    // 进入自循环，调用所有的回调函数（当接收到消息）
    ros::spin();
    return 0;
}


