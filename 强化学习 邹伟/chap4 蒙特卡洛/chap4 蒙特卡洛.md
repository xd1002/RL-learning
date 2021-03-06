# chap4 蒙特卡洛

1. 计算状态平均回报的两种方法：第一次访问蒙特卡洛方法（初访法）和每次访问蒙特卡洛方法（每访法）

   * 初访法：计算状态$s$处的值函数时，只利用每个轨迹中第一次访问到状态$s$的累计回报
     $$
     V(s_1)=\frac{G_{12}+G_{2k}+\cdots}{N(s_1)}
     $$
     如上式所示，$G_{12}$表示第一个轨迹中第一次出现$s_1$在第二步的时候，$G_{2k}$表示第二个轨迹中第一次出现$s_1$在第$k$步的时候，$N(s_1)$表示出现$s_1$的轨迹数

   * 每访法：计算状态$s$处的值函数时，利用所有访问到状态$s$的累计回报
     $$
     V(s_1)=\frac{G_{12}+G_{1k}+G_{2t}+\cdots}{N(s_1)}
     $$
     如上式所示，$G_{12}$表示第一个轨迹中在第二步出现了$s_1$，$G_{1k}$表示第一个轨迹中在第$k$步出现$s_1$，$G_{2t}$表示第二个轨迹中在第$t$步出现了$s_1$，$N(s_1)$表示$s_1$的出现总数