##  【函数型数据子空间聚类】Functional subspace clustering with applications to time series研究

### 任务完成情况

2017.10.30 理解了函数型数据，明白了子空间聚类的原理，算法实际细节过程还需要好好看

函数型数据的聚类方法也逐渐成熟[15-19]，主要分为三类：降维之后使用传统方法聚类（如K-均值、系统聚类等）；采用特殊距离或曲线差异的非参数方法；基于模型的聚类方法。

2017.10.31

### Functional Clustering

TwoSteps支持数值型和分类型数据，这对于我们而言在使用时就方便很多，此外游戏数据一般来说都很大，TwoStep在这方面来说还是很具有优势的，数据迭代过程中的内存消耗和聚类数目确定，TwoStep表现的都很好，两步聚类避免了距离矩阵过大，导致算法执行效率下降，而这也是优势所在。

**步骤及原理**

Step1：预聚类 完成简单数据处理，以便将原始输入数据压缩为可管理的子聚类集合；第一步用到的算法 BIRCH Balanced Iterative Reducing and Clustering using Hierarchies，该算法适合大的数据集，最小化运行时间和数据扫描

*具体过程* 这一步骤通过构建和修改聚类特征树（Cluster Feature Tree）完成。聚类特征数包含许多层的节点，每一节点包含若干个条目，而每一个叶子节点代表一个子类，有多少个叶子就有多少个子类。而那些叶子节点和其中的条目用来指引新进入的记录应该进入那个叶子节点，每个条目中的信息就是所谓的聚类特征（Cluster Feature），包括针对连续变量的均值和方差以及针对离散变量的记数。针对每一个记录，都要从根开始进入聚类特征数，并依照节点中条目信息的指引找到最接近的子节点，直到到达叶子节点为止。如果这一纪录与叶子节点中的距离小于临界值，那么它进入该子节点，并且子节点的聚类特征得到更新，反之，该纪录会重新生成一个新的叶子节点。如果这时子节点的数目已经大于指定的最大聚类数量，则聚类特征树会通过调整距离临界值的方式重新构建。当所有的记录通过上面的方式进入聚类特征树，预聚类过程也就结束了，子节点的数量就是预聚类数量。

Step2：使用层级聚类方法将子聚类一步一步合并为更大的聚类

*具体过程* 将第一步完成的预聚类作为输入，对之进行聚类，直到使用者指定的类别。由于在这个阶段所需处理的类别已经远小于原始数据的数量，所以我们可以采用传统的聚类方法进行处理就可以了。其中在层次聚类的每一个阶段，都会计算反映现有分类是否适合现有数据的统计指标：AIC（Akaike Information Criterion），或者BIC（Schwartz Bayesian Criterion）准则，这两个指标越小，说明聚类效果越好，两步聚类算法会根据AIC和BIC的大小，以及类间最短距离的变化来确定最优的聚类类别数。

优点：就是能够为训练数据自动估计最佳聚类数

**Code ** 待补充

[twostep原理实践讲的比较好](https://wenku.baidu.com/view/41ddb2513c1ec5da50e270da.html)

[SPSS中TwoStep简单运用，数据分析中SPSS也要好好学习啊](http://www.cnblogs.com/yuyang-DataAnalysis/archive/2012/06/14/2549662.html)

[又是一个SPSS中的二阶聚类](http://blog.sina.com.cn/s/blog_13ea9a2450102wzjz.html)

[两步聚类法 改进的BIRCH算法](http://www.cnblogs.com/tiaozistudy/p/twostep_cluster_algorithm.html)

[函数型数据分析（中文论文，不详细）](http://www.stats.gov.cn/tjzs/tjsj/tjcb/dysj/201705/t20170522_1496324.html)

[函数型数据聚类直观理解](https://wenku.baidu.com/view/1097ca5c43323968011c92cb.html)

### subspace Clustering

[子空间算法（PCA）](http://blog.csdn.net/u014230646/article/details/51615808)

[采用属性聚类的高位子空间聚类算法](https://wenku.baidu.com/view/deacabc79ec3d5bbfd0a74af.html)

[CLIQUE聚类算法](http://www.cnblogs.com/1zhk/p/4676671.html)

[子空间聚类问题PPT](http://www.taodocs.com/p-478979.html)

[子空间聚类的一篇硕士论文](http://www.doc88.com/p-7156387057840.html)

#### sparse subspace clustering

#### spectral clustering

##### DTW 



[dtw c实现](http://blog.csdn.net/kingskyleader/article/details/6244011)



### 参考资料

[关于聚类综述的一篇论文](http://www.doc88.com/p-33546313611.html)

[函数型数据分析](http://www.ixueshu.com/document/b558c3ef03fe77e9.html)

[子空间聚类分析](https://baike.baidu.com/item/%E5%AD%90%E7%A9%BA%E9%97%B4%E8%81%9A%E7%B1%BB%E5%88%86%E6%9E%90/15706757?fr=aladdin)

[science发表的一个聚类算法](http://blog.jobbole.com/72540/)

[谱聚类原理实例讲解](http://www.cnblogs.com/vivounicorn/archive/2012/02/10/2343377.html)

[谱聚类算法带例子详解](http://www.cnblogs.com/wentingtu/archive/2011/12/22/2297426.html)

[DTW 时间序列中的一种距离度量](http://blog.csdn.net/zouxy09/article/details/9140207) ：DTW所要做的事情就是选择一个路径，使得最后得到的总的距离最小。

[从DTW到HMM](http://www.cnblogs.com/tornadomeet/archive/2012/03/23/2413363.html)

[L0、L1、L2范数的定义](http://www.cnblogs.com/little-YTMM/p/5879093.html)



### 感兴趣的方面

[协同过滤入门好例子](http://www.cnblogs.com/wentingtu/archive/2011/12/16/2289926.html)

[小白雪数据分析系列教程](http://www.cnblogs.com/yuyang-DataAnalysis/tag/%E5%B0%8F%E7%99%BD%E5%AD%A6%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/)