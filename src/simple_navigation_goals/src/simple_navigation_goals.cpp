#include "ros/ros.h"
#include "std_msgs/Float64MultiArray.h"
#include "move_base_msgs/MoveBaseAction.h"
#include "actionlib/client/simple_action_client.h"
#include <cstdio>

const int key_points = 3;

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
ros::Subscriber sub;
int id;
double rad[key_points],x_rad,y_rad,x[key_points]={1,3,5},y[key_points]={0,0,0};
double x_real[key_points],y_real[key_points];
bool flag[key_points];

// 回调函数
void radiation_sub(const std_msgs::Float64MultiArray msg_s){
    // 通过msg_p来获取并操作订阅到的数据
    // ROS_INFO("meow %f\n",msg_s.data);
    if(!flag[id]){
        // flag[id]=true;
        // rad[id]=msg_s.data[0];
        // x_real[id]=msg_s.data[1];
        // y_real[id]=msg_s.data[2];
        rad[id]=msg_s.data.at(0);
        x_real[id]=msg_s.data.at(1);
        y_real[id]=msg_s.data.at(2);
    }
}

double dist_sqr(double x1,double y1,double x2,double y2){
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2);
}

void get_rad_xy(){
    double ans=100;
    for(double i=0;i<6;i+=0.1){ // 枚举辐射源 x 坐标
        for(double j=-6;j<0;j+=0.1){ // 枚举辐射源 y 坐标
            double t1=(rad[2]-rad[0])/(rad[1]-rad[0]);
            double t2=(1/dist_sqr(x_real[2],y_real[2],i,j)-1/dist_sqr(x_real[0],y_real[0],i,j))
                /(1/dist_sqr(x_real[1],y_real[1],i,j)-1/dist_sqr(x_real[0],y_real[0],i,j));
            if(ans>fabs(t1-t2)){ // 记录最接近的结果
                ans=fabs(t1-t2);
                x_rad=i;
                y_rad=j;
            }
        }
    }
}

int main(int argc, char** argv){
    ros::init(argc, argv, "simple_navigation_goals");
    ros::NodeHandle nh;
    sub=nh.subscribe<std_msgs::Float64MultiArray>("radiation",20,radiation_sub);
    // 建立通信
    MoveBaseClient ac("move_base", true);
    // 要发送的目标
    move_base_msgs::MoveBaseGoal goal;
    // 等待服务启动
    while(!ac.waitForServer(ros::Duration(5.0))){
        ROS_INFO("Waiting for the move_base action server to come up");
    }
    // 设置要发送的目标
    goal.target_pose.header.frame_id = "map";
    goal.target_pose.header.stamp = ros::Time::now();
    goal.target_pose.pose.position.z = 0.0;
    goal.target_pose.pose.orientation.x = 0.0;
    goal.target_pose.pose.orientation.y = 0.0;
    goal.target_pose.pose.orientation.z = 0.0;
    goal.target_pose.pose.orientation.w = 1.0;

    for(int i=0;i<key_points;++i){
        // 到达第i个点并收集辐射信号
        ROS_INFO("%d?",i);
        goal.target_pose.pose.position.x = x[i];
        goal.target_pose.pose.position.y = y[i];
        // 发送目标
        ac.sendGoal(goal);
        // 等待结果
        ac.waitForResult();
        id=i;
        // 调用一次 Subscriber 的回调函数
        ros::spinOnce();
        ROS_INFO("%d!",i);
    }

    get_rad_xy();

    /*
    FILE *fout=fopen("/home/ucar/ucar_ws/rad_info.txt","w");
    fprintf(fout,"%lf %lf\n",x_rad,y_rad);
    fclose(fout);
    */
    
    FILE *fout=fopen("/home/kiwi/SmartCar/smart-car/rad_info.txt","w");
    fprintf(fout,"%lf %lf\n",x_rad,y_rad);
    fclose(fout);

    goal.target_pose.pose.position.x = x_rad;
    goal.target_pose.pose.position.y = y_rad;
    ROS_INFO("meow %lf %lf\n",x_rad,y_rad);
    ac.sendGoal(goal);
    ac.waitForResult();
    return 0;
}
