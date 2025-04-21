# README

### 1. 技术和方法

#### 1.1 路径规划算法
##### a. 全局规划路径：Dijkstra算法
在实际实现过程中，我们发现Dijkstra算法相对于A*算法效果更好，且其由于遍历所有可能路径而带来的计算成本在此比赛中可忽略不计，故选取Dijkstra算法。


相关参数详见`src\nav\launch\config\move_base\global_planner_params.yaml`

##### b. 局部规划路径：TEB算法
**TEB**(Time Elastic Band) 算法通过优化时间弹性带，能够在动态环境中生成平滑且高效的局部路径。其主要特点是将时间和空间约束结合到路径优化中，适用于复杂的动态场景。相对于DWA算法，TEB算法能够在一定程度上减少路径的弯曲程度，提高路径的平滑度。
- **1.** 关键参数在于角速度`max_vel_theta`的修改，使得小车在进行转弯时能够在有限空间中掉转车头，极大降低了撞墙的概率，其目前形式效果略显秋名山车神风范。
- **2.** 其参数详见`src\nav\launch\config\move_base\teb_local_planner_params.yaml`
- **3.** 在执行过程中，为了适配TEB算法结构，我们对相同目录下`yaml`文件中参数与结构进行了微调，详见`1`中其他文件。
   
#### 1.2 辐射源算法
采用优化算法求解辐射源问题，使用Levenberg-Marquardt算法求解优化问题。
##### a. Levenberg-Marquardt算法
Levenberg-Marquardt算法是一种用于非线性最小二乘问题的优化算法。它主要用于拟合一个非线性模型以匹配一组数据，通常是通过最小化实际数据点与拟合曲线之间的误差平方和来实现的。

###### 原理

Levenberg-Marquardt算法结合了梯度下降法和高斯-牛顿法的优点。在高斯-牛顿法中，每次迭代都使用线性近似来更新参数，这种方法在接近最优解时表现良好，但在远离最优解时可能会遇到问题，比如陷入局部最小值或发散。而梯度下降法则更为稳健，尤其是在参数远离最优值时，但其收敛速度较慢。

Levenberg-Marquardt算法通过引入一个阻尼参数λ来控制每次迭代的步长，当远离最优解时，λ较大，步长较小，有利于稳定性；而当接近最优解时，λ较小，步长较大，有利于快速收敛。

###### 迭代公式

在每次迭代中，Levenberg-Marquardt算法更新参数的方式为：

$ \Delta x = (J^T J + \lambda I)^{-1} J^T r $

其中，$J$是雅可比矩阵，$r$是残差向量，$I$是一个单位矩阵，$\lambda$是阻尼因子。

##### b. 具体实现
- 首先我们人为给出不同辐射源数量下的均方误差优化函数：

$$
\sum^N_{i=1} (I_i - \frac{k_1}{(x_i-X_1)^2+(y_i-Y_1)^2}-\frac{k_2}{(x_i-X_2)^2+(y_i-Y_2)^2})^2 \\

\sum^N_{i=1} (I_i - \frac{k_1}{(x_i-X_1)^2+(y_i-Y_1)^2})^2
$$

- 小车在左侧走廊中采集一定数量的点的坐标及对应坐标的辐射强度
- 利用Levenberg-Marquardt算法求解优化问题，求得最优的辐射源参数。在这里我们首先将强度最大的点作为初始值，然后通过Levenberg-Marquardt算法迭代更新参数。然后我们将得到的解作为初始值，再次利用Levenberg-Marquardt算法迭代更新参数。实验中取得了很好的效果。
- 使用scipy中的`optimize.least_squares`函数实现Levenberg-Marquardt算法


#### 1.3 其他创新

- **恢复行为**：局部代价地图增加了**恢复行为**(Recovery Behaviors)，修改见`src\nav\launch\config\move_base\local_costmap_params.yaml`

*注： 恢复行为即在小车导航陷入停滞时尝试刷新周围的障碍物信息，然后重新进行路径规划，试图让小车回到正轨上。*

---

### 2. 环境配置

#### 2.1 依赖环境
- **操作系统**：Ubuntu 18.04
- **ROS版本**：Melodic
- **ros依赖库**：
  - `ros-melodic-teb-local-planner`
  - `ros-melodic-amcl`
  - `ros-melodic-move-base`
  - `ros-melodic-rviz`
- **python依赖库**：*要求在电脑上配置Python版本>=3.6，且将高版本的Python加入环境变量，并设置为默认版本。*
  - `numpy`
  - `scipy`
#### 2.2 复现步骤
- **1.** 安装ROS Melodic，安装依赖库
- **2.** 将新的地图参数放在`src\nav\maps`目录下，要求新添加的地图按照原有文件命名格式命名
- **3.** 运行`bash ./launch.sh`，查看单一辐射源情况效果
- **4.** 运行`bash ./launch2.sh`，查看双辐射源情况效果
- **5.** 将会在目录下的`rad_info.txt`中保存辐射源信息，主要包括位置信息(双辐射源情况下无法对两个辐射源进行区分，顺序可能有区别)
