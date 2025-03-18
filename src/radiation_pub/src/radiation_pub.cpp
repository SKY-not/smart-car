#include "ros/ros.h" // 统一头文件
#include "nav_msgs/Odometry.h" // 订阅的消息类型
#include "std_msgs/Float64MultiArray.h" // 发布的消息类型
#include <vector> // 向量（数组），用于给发布的消息赋值


// 辐射源位置和系数，仅供调试，初赛测试时会改变
// 不保证辐射源位置只有一位小数
const double x_rad = 0;
const double y_rad = -5.7;
const double k = 20;

// 订阅器和发布器
ros::Subscriber sub;
ros::Publisher pub;

double dist_sqr(double x1,double y1,double x2,double y2){
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2);
}

// 回调函数
void radiation_pub(const nav_msgs::Odometry msg_s){
    // 通过 msg_p 来获取并操作订阅到的数据
    double x,y;
    x=msg_s.pose.pose.position.x;
    y=msg_s.pose.pose.position.y;

    // 先把要发布的数据存入 vector
    std::vector<double> vec;
    vec.push_back(k/dist_sqr(x,y,x_rad,y_rad));
    vec.push_back(x);
    vec.push_back(y);

    // 通过 msg_s 来操作要发布的数据
    std_msgs::Float64MultiArray msg_p;
    msg_p.data = vec;
    pub.publish(msg_p);

}
 
int main(int argc, char *argv[])
{
    // 节点初始化
    ros::init(argc,argv,"radiation_pub");
    // 实例化 ROS 句柄
    ros::NodeHandle nh;
    // 实例化订阅者对象,参数1是话题名(要保证和发布方的话题一致)
    // 参数2是buffer空间大小，参数3是回调函数
    sub = nh.subscribe<nav_msgs::Odometry>("odom",200,radiation_pub);
    // 实例化发布者对象，参数是话题名，buffer大小
    pub = nh.advertise<std_msgs::Float64MultiArray>("radiation",20);
    // 进入自循环，调用所有的回调函数（当接收到消息）
    ros::spin();
    return 0;
}


