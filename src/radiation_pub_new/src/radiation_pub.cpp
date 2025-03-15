#include "ros/ros.h"
#include "nav_msgs/Odometry.h"
#include "std_msgs/Float64MultiArray.h"
#include <cmath>
#include <vector>

const double x_rad = 0;
const double y_rad = -5.7;

ros::Subscriber sub;
ros::Publisher pub;
 
// 回调函数
void radiation_pub(const nav_msgs::Odometry msg_s){
    // 通过msg_p来获取并操作订阅到的数据
    double x,y;
    x=msg_s.pose.pose.position.x;
    y=msg_s.pose.pose.position.y;
    std::vector<double> vec;
    vec.push_back(20/((x-x_rad)*(x-x_rad)+(y-y_rad)*(y-y_rad)));
    vec.push_back(x);
    vec.push_back(y);
    std_msgs::Float64MultiArray msg_p;
    msg_p.data = vec;
    pub.publish(msg_p);

}
 
int main(int argc, char *argv[])
{
    //节点初始化
    ros::init(argc,argv,"radiation_pub");
    // 实例化 ROS 句柄
    ros::NodeHandle nh;
    // 实例化订阅者对象,参数1是话题名(要保证和发布方的话题一致)，参数2是buffer空间大小，参数3是回调函数
    sub=nh.subscribe<nav_msgs::Odometry>("odom",100,radiation_pub);
    // 实例化发布者对象，参数是话题名，buffer大小
    pub = nh.advertise<std_msgs::Float64MultiArray>("radiation",10);
    //进入自循环，调用所有的回调函数（当接收到消息）
    ros::spin();
    return 0;
}
 
