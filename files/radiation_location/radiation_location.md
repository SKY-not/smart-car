# 辐射源自动定位

## 辐射源
辐射源辐射强度按照平方反比方式衰减，

## 可能的实现方法
### 线性化转换法（最小二乘法）
#### 1.线性化
将平方反比公式线性化得到：
$$\frac{1}{I}=\frac{(x-x_0)^2+(y-y_0)^2}{k}$$
进一步展开可以得到：
$$\frac{1}{I}=\frac{x^2+y^2}{k}-\frac{2x_0x}{k}-\frac{2y_0y}{k}+\frac{x_0^2+y_0^2}{k}$$
作变量代换：
$$A=\frac{1}{k},B=-\frac{2x_0}{k},C=-\frac{2y_0}{k},D=\frac{x_0^2+y_0^2}{k}$$
则：
$$\frac{1}{I}=A(x^2+y^2)+Bx+Cy+D$$
#### 2.最小二乘法求解参数
对于每一个数据点$(x_i,y_i,I_i)$，构建线性方程：
$$A(x_i^2+y_i^2)+Bx_i+Cy_i+D=\frac{1}{I_i}$$
求解参数$A,B,C,D$，使得方程的残差平方和最小。
反向计算辐射源参数：
$$x_0=-\frac{B}{2A},y_0=-\frac{C}{2A},k=\frac{1}{A}$$
进一步可以验证
$$D=\frac{B^2+C^2}{4A}$$
是否在精度范围内成立从而检查合理性

### 3.优势与不足
计算复杂度低O(n)，适合百万级数据点，可在毫秒级完成

### 非线性优化法
将线性化结果作为初值，优化目标函数，使得目标函数最小：
$$
min_{x_0,y_0,k}\sum_{i=1}^N I_i-\frac{k}{(x_i-x_0)^2+(y_i-y_0)^2}
$$

