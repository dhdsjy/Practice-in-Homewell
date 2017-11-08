# Hadoop生态系统之Hbase

- Nutch，互联网数据及Nutch搜索引擎应用
-  HDFS,Hadoop的分布式文件系统
- MapReduce,分布式计算框架
- Flume、Scribe，Chukwa数据收集，收集非结构化数据的工具。
- Hiho、Sqoop,讲关系数据库中的数据导入HDFS的工具
- Hive数据仓库，pig分析数据的工具
- Oozie作业流调度引擎 
- Hue，Hadoop自己的监控管理工具
- Avro 数据序列化工具
- mahout数据挖掘工具
- Hbase分布式的面向列的开源数据库

## Hadoop是什么

Hadoop是一个开源框架，可编写和运行分布式应用处理大规模数据。 Hadoop框架的核心是HDFS和MapReduce。其中 HDFS 是分布式文件系统，MapReduce 是分布式数据处理模型和执行环境。

**优势**

1. 运行方便：Hadoop是运行在由一般商用机器构成的大型集群上。Hadoop在云计算服务层次中属于PaaS(Platform-as-a- Service)：平台即服务。 
2. 健壮性：Hadoop致力于在一般的商用硬件上运行，能够从容的处理类似硬件失效这类的故障。 
3. 可扩展性：Hadoop通过增加集群节点，可以线性地扩展以处理更大的数据集。 
4. 简单：Hadoop允许用户快速编写高效的并行代码。

hadoop 2.0 生态系统



![img](http://i.imgur.com/Dpz74XZ.jpg)![img](http://i.imgur.com/x40qGJk.jpg)



### HDFS 分布式文件系统

**特点**

+ 良好的扩展性
+ 高容错性
+ 适合PB级以上海量数据的存储

**基本原理**

+ 将文件切分成等大的数据块，存储到多台机器上
+ 将数据切分、容错、负载均衡等功能透明化
+ 可将HDFS看成容量巨大、具有高容错性的磁盘

**应用场景**

+ 海量数据的可靠性存储
+ 数据归档

### Yarn 资源管理系统

Yarn是Hadoop2.0新增的系统，负责集群的资源管理和调度，使得多种计算框架可以运行在一个集群中。

**特点**

1. 良好的扩展性、高可用性
2. 对多种数据类型的应用程序进行统一管理和资源调度
3. 自带了多种用户调度器，适合共享集群环境

![img](http://i.imgur.com/d70zXQK.jpg)

### MapReduce 分布式计算框架

![img](http://i.imgur.com/wXUseY2.jpg)

### Hive 基于MR的数据仓库

Hive由facebook开源，最初用于解决海量结构化的日志数据统计问题；是一种ETL(Extraction-Transformation-Loading)工具。它也是构建在Hadoop之上的数据仓库；数据计算使用MR,数据存储使用HDFS。Hive定义了一种类似SQL查询语言的HiveQL查询语言，除了不支持更新、索引和实物，几乎SQL的其他特征都能支持。它通常用于离线数据处理（采用MapReduce);我们可以认为Hive的HiveQL语言是MapReduce语言的翻译器，把MapReduce程序简化为HiveQL语言。但有些复杂的MapReduce程序是无法用HiveQL来描述的。

**Hive 应用场景**

1. 日志分析：统计一个网站一个时间段内的pv、uv ；比如百度。淘宝等互联网公司使用hive进行日志分析
2. 多维度数据分析
3. 海量结构化数据离线分析
4. 低成本进行数据分析（不直接编写MR）                                                           

![img](http://i.imgur.com/tGvdpMn.jpg)



### Pig 数据仓库

Pig是构建在Hadoop之上的数据仓库，定义了一种类似于SQL的数据流语言–Pig Latin,Pig 
Latin可以完成排序、过滤、求和、关联等操作，可以支持自定义函数。Pig自动把Pig 
Latin映射为MapReduce作业，上传到集群运行，减少用户编写Java程序的苦恼。

![img](http://i.imgur.com/90OiAtM.jpg)

### Mahout 数据挖掘

![img](http://i.imgur.com/2kMHImL.jpg)

### Zookeeper

Zookeeper解决分布式环境下数据管理问题：

1. 统一命名
2. 状态同步
3. 集群管理
4. 配置同步

### Sqoop 数据同步工具

Sqoop是连接Hadoop与传统数据库之间的桥梁，它支持多种数据库，包括MySQL、DB2等；插拔式，用户可以根据需要支持新的数据库。Sqoop实质上是一个MapReduce程序，充分利用MR并行的特点,充分利用MR的容错性。

![img](http://i.imgur.com/aNVqEER.jpg)

### Flume 日志收集工具

**特点**

1. 分布式
2. 高可靠性
3. 高容错性
4. 易于定制与扩展

### Oozie 作业调度系统

目前计算框架和作业类型种类繁多：如MapReduce、Stream、HQL、Pig等。这些作业之间存在依赖关系，周期性作业，定时执行的作业，作业执行状态监控与报警等。如何对这些框架和作业进行统一管理和调度？![img](http://i.imgur.com/mbk9kJX.jpg)

### Hbase 分布式数据库

HBase可以使用shell、web、api等多种方式访问。它是NoSQL的典型代表产品。

**特点**

1. 存储容量大，一个表可以有数十亿行，上百万列；
2. 无模式：每行都有一个可排序的主键和任意多的列，列可以根据需要动态的增加，同一张表中不同的行可以有截然不同的列；
3. 面向列 面向列（族）的存储和权限控制，列（族）独立检索；
4. 稀疏 ：空（null）列并不占用存储空间，表可以设计的非常稀疏；
5. 数据多版本：每个单元中的数据可以有多个版本，默认情况下版本号自动分配，是单元格插入时的时间戳；
6. 数据类型单一：Hbase中的数据都是字符串，没有类型。

![img](http://i.imgur.com/4FdwBFG.jpg)

- Table（表）：类似于传统数据库中的表
- Column Family(列簇)：Table在水平方向有一个或者多个Column Family组成；一个Column Family 中可以由任意多个Column组成。
- Row Key(行健)：Table的主键；Table中的记录按照Row Key排序。
- Timestamp（时间戳）：每一行数据均对应一个时间戳；也可以当做版本号。

**Hbase 数据模型**

+ Hbase 逻辑视图

![img](http://i.imgur.com/URUpR4i.png)

![img](http://img.blog.csdn.net/20131226173226562?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd29zaGl3YW54aW4xMDIyMTM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ **Hbase物理模型**

![img](http://i.imgur.com/f2FSBal.png)

#### Hbase中的一些基本概念

+ Row Key 用来检索记录的主键，访问Hbase中的行，只有三种方式：
  + 通过单个容Row Key 访问
  + 通过Row Key的range全表扫描
  + 行的一次读写是原子操作（不论一次读写多少列）。这个设计决策能够使用户很容易理解程序在对同一个行进行并发更新操作时的行为。
+ 列族 HBase 表中的每个列都归属于某个列族。列族是表的 Schema 的一部分（而列不是），必须在使用表之前定义。列名都以列族作为前缀，例如 courses:history、courses:math 都属于 courses 这个列族。
+ 时间戳 HBase 中通过 Row 和 Columns 确定的一个存储单元称为 Cell。每个 Cell 都保存着同一份数据的多个版本。 版本通过时间戳来索引，时间戳的类型是 64 位整型。时间戳可以由HBase（在数据写入时自动）赋值， 此时时间戳是精确到毫秒的当前系统时间。时间戳也 可以由客户显示赋值。如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳。每个 Cell 中，不同版本的数据按照时间倒序排序，即最新的数据排在最前面。
+ Cell Cell 是由 {row key，column(=< family> + < label>)，version} 唯一确定的单元。Cell 中的数据是没有类型的，全部是字节码形式存储

#### Hbase数据库与shell命令

+ 一般操作 

  + status 查询服务器状态
  + whoami 查询当前用户
  + version 当前hbase版本号

+ 表操作

  + list 查看已存在的表

  + create 创建数据库表  create <table>,{NAME =><columnfamily>,VERSIONS =><versions>}

    ```
    # 创建一张表product，并且创建2个列族，分别为computer和food
    create 'product', {NAME=>'computer',VERSIONS=>5},{NAME=>'food',VERSIONS=>3}
    ```

  + describe 查看表结构描述

    ```
    describe ‘product’
    ```

  + **alter** 操作顺序：disable->修改表->enable 可以修改已存在的数据，也可以增加一个列族

    ```
    disable 'product'
    alter 'product',{NAME=>'food',VERSIONS=>5}
    enable 'product'
    ```

  + **drop** disable->drop

    ```
    disable 'product'
    drop 'product'
    ```

+ 增删改查操作

  + **增** put 插入数据 put <table>,<rowkey>,<<family:column>>,<value>,<timestamp>

    ```
    put 'product','rowkey001','computer:name','ThinkPad E550'
    put 'product','rowkey001','computer:price',4199
    ```

  + **删**

    + delete、deleteall 删除行中的某个列值，前者必须指定列名，后者可以不指定，删除整行

      delete <table>,<rowkey>,<<family:column>>,<timestamp>

    ```
    delete 'product','rowkey001','computer:name'
    ```

    + truncate 删除表中所有数据 truncate <table>

  + **改** 见alter部分

  + **查**

    + scan 扫描整张表 scan <table>,{columns=>[<<family:column>>,...],limit=>num}

    ```
    scan 'xuwftest',{COLUMNS=>['computer:price','computer:name']}/不要忘记大括号和columns
    ```

    + get 查询某个cell的数据

      ```
      get 'xuwftest','rowkey001'
      get 'xuwftest','rowkey001',['computer:name']
      ```

    + count 查询表中数据行数 count <table>,{INTERVAL=>intervalNum,CACHE=>cacheNum};INTERVAL设置多少行显示一次及对应的rowkey，默认1000，CACHE每次去取的缓存大小，默认为10，调整该参数可提高查询速度

      ```
      count 'product',{INTERVAL=>10,CACHE=>1000}
      ```

      ​

  