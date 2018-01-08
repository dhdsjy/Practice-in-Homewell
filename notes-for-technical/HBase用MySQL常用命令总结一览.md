# HBase用MySQL常用命令总结一览

### Mysql 篇

#### 准备

+ 打开工作环境 mysql -u root -p
+ 连接远程主机上的MySQL mysql -h 110.110.110.110 -u root -p 123
+ 退出MySQL exit

#### 常用命令

##### 数据库操作

+ 创建数据库 CREATE DATABASE 数据库名;

+ 查看当前数据库状态 STATUS；

+ 删除数据库 DROP DATABASE 数据库名；

+ 连接数据库/切换数据库 USE 数据库名；（注意：**使用USE语句为一个特定的当前的数据库做标记，不会阻碍您访问其它数据库中的表**）

+ 查看当前使用的数据库 select database(); sql中的select 相当于其他语言中的print

+ 显示数据库 SHOW DATABASES；SHOW TABLES;显示当前数据库下所有表的名称

+ 备份（导出）数据库　导出文件默认存在mysql\bin；也可以指定路径，但在备份的时候一定要进入mysql的安装目录　cd /usr/local/mysql 

   **mysqldump -u root -p密码 数据库名  数据表名 >  /filepath/mysql.sql**

  ```
  [root@localhost ~]# cd /var/lib/mysql(进入到MySQL库目录，根据自己的MySQL的安装情况调整目录)
  [root@localhost mysql]# mysql -u root -p voice<voice.sql，输入密码即可。

  用 source 语句
  mysql -u dbadmin -p
  use myblog;
  set names utf8;  #这里的字符集根你的将要导入的数据库的字符集一至。
  source /home/zhangy/blog/database_bak/myblog.sql;
  ```

  ​

##### 表操作

+ 创建数据表 **命令：create table <表名> ( <字段名1> <类型1> [,..<字段名n> <类型n>]);**

  + **MySQL中常见的数据类型**

    + 整数类型 **int**
    + 浮点型 **float/double/dec(m,d)** 在对数据要求较高的情况下，选择dec更安全，m表示精度，数据总长度，d表示标度，小数点后的长度
    + 字符型 **char ** 固定长度，处理速度快；**varchar**  实际占用空间为字符串实际长度加1，占用空间小，灵活
    + 二进制性 **bit(M)**  M’指定了该二进制数的最大字节长度为M，M的最大值为64;
    + 日期时间类型 **DATETIME、 TIMESTAMP、DATE、TIME、YEAR**  [日期时间类型](https://www.cnblogs.com/Jie-Jack/p/3793304.html)

    | 日期时间类型    | 占用空间    | 日期格式                | 最小值                 | 最大值                 | 零值表示                |
    | --------- | ------- | ------------------- | ------------------- | ------------------- | ------------------- |
    | DATETIME  | 8 bytes | YYYY-MM-DD HH:MM:SS | 1000-01-01 00:00:00 | 9999-12-31 23:59:59 | 0000-00-00 00:00:00 |
    | TIMESTAMP | 4 bytes | YYYY-MM-DD HH:MM:SS | 19700101080001      | 2038 年的某个时刻         | 00000000000000      |
    | DATE      | 4 bytes | YYYY-MM-DD          | 1000-01-01          | 9999-12-31          | 0000-00-00          |
    | TIME      | 3 bytes | HH:MM:SS            | -838:59:59          | 838:59:59           | 00:00:00            |
    | YEAR      | 1 bytes | YYYY                | 1901                | 2155                | 0000                |

  + **MySQL常见的完整性约束**

    + **PRIMARY KEY** 标识该属性为该表的主键，可以是单一字段，也可以是多个字段组合

      + 单字段主键 属性名 数据类型 PRIMARY KEY

      + 多字段主键，一般是在属性定义完，统一设置主键

        ```
        CREATE TABLE example (std_id int,
                              course_id int,
                              grade float,
                              primary key (std_id,course_id));
        ```

    + **FOREIGN KEY**  标识该属性为该表的外键，是与之联系的某表主键；其中最常见创建外键的格式是：constraint FK_*（外键别名） foreign key(**) references 链接的外表

      ```
      如果一个实体的某个字段指向另一个实体的主键，就称为外键,被指向的实体，称之为主实体（主表），也叫父实体（父表）。负责指向的实体，称之为从实体（从表），也叫子实体（子表）
      ```

      ![primary key & foreign key](http://images.cnitblog.com/i/563678/201407/301646292121112.x-png)

      + 级联（cascade）方式创建外键引用关系　关键字　on delete on update;关联操作，如果主表被更新或删除，从表也会执行相应的操作

        ```
        # 创建用户组
        mysql> create table t_group(
            -> id int not null,
            -> name varchar(30),
            -> primary key (id));
        Query OK, 0 rows affected (0.57 sec)

        mysql> insert into t_group values (1,"Group1");
        Query OK, 1 row affected (0.05 sec)
        mysql> insert into t_group values (2,'Group2');
        Query OK, 1 row affected (0.09 sec)

        mysql> select * from t_group;
        +----+--------+
        | id | name   |
        +----+--------+
        |  1 | Group1 |
        |  2 | Group2 |
        +----+--------+
        2 rows in set (0.00 sec)

        # 创建用户
        mysql> create table t_user(
            -> id int not null,
            -> name varchar(30),
            -> groupid int,
            -> primary key (id),
            -> foreign key (groupid) references t_group(id) on delete cascade on update cascade);　级联方式
            -> foreign key (groupid) references t_group(id) on delete set null on update set null 置空方式
            ->foreign key (groupid) references t_group(id) on delete no action on update no action　禁止方式
        Query OK, 0 rows affected (0.39 sec)

        **注意** :添加外键约束时若没有指定外键约束的名称，则系统会自动添加外键约束名：表名_ibfk_n(表示第n个外键约束)

        mysql> insert into t_user values (1,'qianxin',1);
        Query OK, 1 row affected (0.05 sec)
        mysql> insert into t_user values (2,'yiyi',2);
        Query OK, 1 row affected (0.04 sec)
        mysql> insert into t_user values (3,'dai',2);
        Query OK, 1 row affected (0.09 sec)

        # 级联威力
        mysql> delete from t_group where id=2;
        Query OK, 1 row affected (0.07 sec)

        mysql> select * from t_group;
        +----+--------+
        | id | name   |
        +----+--------+
        |  1 | Group1 |
        +----+--------+
        1 row in set (0.00 sec)

        mysql> select * from t_user;
        +----+---------+---------+
        | id | name    | groupid |
        +----+---------+---------+
        |  1 | qianxin |       1 |
        +----+---------+---------+
        1 row in set (0.00 sec)

        mysql> update t_group set id=2 where id=1;
        Query OK, 1 row affected (0.08 sec)
        Rows matched: 1  Changed: 1  Warnings: 0

        mysql> select * from t_group;
        +----+--------+
        | id | name   |
        +----+--------+
        |  2 | Group1 |
        +----+--------+
        1 row in set (0.00 sec)

        mysql> select * from t_user;
        +----+---------+---------+
        | id | name    | groupid |
        +----+---------+---------+
        |  1 | qianxin |       2 |
        +----+---------+---------+
        1 row in set (0.00 sec)
        ```

      + 置空（set null）方式  表示从表数据不指向主表任何记录

        和级联方式效果差不多，只是在主表中的任何操作映射到从表中，所有的操作均将从表设置为NULL.

      + 禁止（no action/restrict）方式 拒绝主表的相关操作

        和级联方式效果差不多，只是在主表中的属性和从表有关，皆不可操作

    + **AUTO_INCREMENT** 标识该属性的值自动增加,一个表中只能有一个字段使用该约束，且该字段必须为主键的一部分 ;所以在插入时，不用指定该属性的值

    + **UNIQUE** 标识该属性值是唯一的

    + **DEFAULT** 为该属性设置默认值

    + **NOT NULL** 标识该属性不能为空

  ```
  create table table1
  (id int(4) not null primary key auto_increment,
  name char(20) not null, 
  sex int(4) not null default '0',
  degree double(16,2));

  mysql> describe table1;
  +--------+--------------+------+-----+---------+----------------+
  | Field  | Type         | Null | Key | Default | Extra          |
  +--------+--------------+------+-----+---------+----------------+
  | id     | int(4)       | NO   | PRI | NULL    | auto_increment |
  | name   | char(20)     | NO   |     | NULL    |                |
  | sex    | int(4)       | NO   |     | 0       |                |
  | degree | double(16,2) | YES  |     | NULL    |                |
  +--------+--------------+------+-----+---------+----------------+
  ```

+ 增删改查

  + insert into 使用INSERT INTO SQL语句来插入数据,如果数据是字符型，必须使用单引号或者双引号，如："value"。

    ```
    INSERT INTO table_name ( field1, field2,...fieldN )
                           VALUES
                           ( value1, value2,...valueN );
    ```

  + 将查询结果插入表中

    ```
    insert into 表名1 (属性列表1) select 属性列表1 from 表名2 where 条件表达式
    ```


  + ---

    drop table 表名；

  + 删除被关联的父表 应先删除子表的外键约束再删除父表

  + 删除数据 删除数据即删除表中已经存在的记录，可以删除表中不再使用的数据。基本语法为

    ```
    delete from 表名 [WHERE 条件表达式]
    ```

    where用来指定待删除的目标记录，如果没有条件表达式，数据库系统就会删除表中的所有数据。 

    注意，系统对删除过程不会有任何提示，所以要谨慎。

    ---

  + ALTER 当我们需要修改数据表名或者修改数据表字段时

    + 增加新的字段　alter table 表名 add 属性名 数据类型 完整性约束条件 [First | After 某属性];

    + 增加外键　alter table 表1名 add foreign key (fk) references 表2名(某字段) on delete cascade;

      ```
      alter table t_user add foreign key(groupid) references t_group(id) on delete cascade;
      ```

    + 删除字段　alter table 表名 drop 属性名;

    + 删除表的外键约束　alter table 表名 drop foreign key 外键别名；

    + 改表名　alter table 旧表名 rename 新表名；

    + 改字段名　alter table 表名 change 旧属性名　新属性名　新数据类型;

    + 改字段数据类型　alter table 表名 modify 属性名　新数据类型；

  + UPDATE 用于修改表中的数据 update 表名 set 列名=新值 where 列名2=某值

    ```
    1、set一个字段
    在表t_test中设置第二条记录（bs为2）的password为'***'。
    update t_test t
       set t.password = '***'
     where t.bs = 2;
     
    2、set多个字段
    在表t_test中设置第一条记录（bs为1）的password为'*'、remark为'*'。
    update t_test t
       set t.password = '*', t.remark = '*'
     where t.bs = 1;
     
    3、set null值
    在表t_test中设置第三条记录（bs为3）的password为null、remark为null。
    update t_test t
       set t.password = null, t.remark = null
     where t.bs = 3;
    ```

    ​

    ---

    + describe 表名；

    + show create table 表名；查看表的详细定义

    + show tables;

    + SELECT 基本查询语句

      ```
      SELECT [DISTINCT] 属性列表/聚合函数  
      FROM 表名/视图 [LIMIT [初始位置【0】],显示记录条数]
      [WHERE 条件表达式1]
      [GROUP BY 属性名1 [HAVING 条件表达式2]] /将查询结果按某个字段或多个字段进行分组，字段中值相等的为一组；WHERE 关键字无法与聚合函数一起使用。 HAVING 子句可以让我们筛选分组后的各组数据
      [ORDER BY 属性名2 [ASC|DESC]]

      example
      1. SELECT count(a.updatetime) FROM udcweb.entity as a;/查询entity表中字段updatetime的数目（不包含缺失值）；count(*)表示返回表中的记录数；COUNT(DISTINCT column_name)返回指定列的不同值的数目
         select count(*) as 个数, 车牌 from table1 group by 车牌 order by count(*) desc 统计每个重复车牌的数目
      select a.name,a.id,Max(a.importuserid) from entity as a 
      where a.name like '家和%' 
      group by a.orgid having count(a.fast > 10000) 
      order by a.importuserid desc limit 10000;
      ```

      - WHERE 查询指定记录 
        - BETWEEN AND 、NOT BETWEEN AND 指定范围(包含等于)   XX [NOT] BETWEEN 取值1 AND 取值2
        - IN、NOT IN 指定集合       XX [NOT] IN (元素1，元素2，...，元素n)
        - LIKE、NOT LIKE 匹配字符 XX [NOT] LIKE '字符串' %表示任意个字符，_表示一个字符，一个汉字是两个字符哦
        - IS NULL、IS NOT NULL是否为空值 XX IS [NOT] NULL
        - AND、OR 多个查询条件  条件表达式1 AND/OR 条件表达式2 [...AND/OR条件表达式n]

    + 连接查询 将多个表按某个条件连接起来，从中选择需要的数据

      - 内连接查询 最常用的连接查询方式，通常将两张表中具有相同意义的字段进行值相等相连

        ```
        select b.*,a.* from organization as b,entity as a
        where b.id = a.orgid limit 1000;

        select s.name,m.mark from student s inner join mark m on s.id=m.studentid
        ```

      - 外连接查询 不仅可以查询出该字段取值相同的记录，也可以查询出该字段取值不相等时的记录，分为左连接和右连接 参数on后面就是连接条件，进行左连接查询时，可以查询出表名1中的所有记录，而表名2中只能查询出匹配的记录

        ```
        # 左连接 将左边的字段全部选出来 所以连接后的记录条数大于等于连接前的条数
        select s.name,m.mark from student s left join mark m on s.id=m.studentid
        # 右连接 右连接就是把右边表的数据全部取出，不管左边的表是否有匹配的数据
        select s.name,m.mark from student s right join mark m on s.id=m.studentid
        # 全连接 把左右两个表的数据都取出来，不管是否匹配
        select s.name,m.mark from student s full join mark m on s.id=m.studentid
        ```

    + 子查询 子查询是将一个查询语句嵌套在另一个查询语句中，即实现多表之间的查询。内层查询语句的查询结果，为外层查询语句提供查询条件。

      - 带比较运算符的子查询 

        ```
        select d_id,d_name from department
        where d_id != 
        (select d_id from employee where age=24)
        ```

      - 综合查询

      ```
      select * from organization as b
      left join
      (select * from entity where id = 1) as a
      on b.id = a.orgid
      ```

    + 合并查询结果 将多个select语句查询结果合并到一起显示；使用UNION时，数据库系统会将所有的查询结果合并到一起然后去除掉相同的记录，类似于进行集合；而使用UNION ALL时，只是将所有查询结果进行简单合并，并不剔除相同的记录。

    + 使用正则表达式查询

      ![正则表达式](http://img.blog.csdn.net/20160413093748539)

---



#### SQL常用内部函数

丰富的函数可以简化用户的操作，让操作更加灵活，此外，由于函数的执行速度非常快，还可以提高MySQL的处理速度。 前面介绍到的Select语句及其条件表达式，Insert、Update和Delete语句及其条件表达式都可以使用这些函数。 MySQL函数包括数学函数、字符串函数、日期和时间函数、条件判断函数、徐彤信息函数、加密函数、格式化函数等。下面将详细介绍这些函数的使用方法。在SQL中，基本的函数类型和种类有若干种，函数的基本类型是：

+ aggregate 函数 Aggregate 函数的操作面向一系列的值，并返回一个单一的值

  + avg(col) 返回某列的平均值 （不包括null值）

  ```
  SELECT AVG(column_name) FROM table_name
  找到 OrderPrice 值高于 OrderPrice 平均值的客户
  SELECT Customer FROM Orders
  WHERE OrderPrice>(SELECT AVG(OrderPrice) FROM Orders)
  ```

  + count(col) 返回某列的行数（不包括null值）

  ```
  SELECT COUNT(column_name) FROM table_name
  SELECT COUNT(*) FROM table_name
  SELECT COUNT(DISTINCT column_name) FROM table_name
  计算客户 "Carter" 的订单数
  SELECT COUNT(Customer) AS CustomerNilsen FROM Orders
  WHERE Customer='Carter'
  表中总行数
  SELECT COUNT(*) AS NumberOfOrders FROM Orders
  计算 "Orders" 表中不同客户的数目
  SELECT COUNT(DISTINCT Customer) AS NumberOfCustomers FROM Orders
  ```

  + FIRST(col) /LAST(col) 返回在指定的域中第一个记录的值/最后一个记录的值

  ```
  SELECT FIRST(column_name) FROM table_name
  查找 "OrderPrice" 列的第一个值
  SELECT FIRST(OrderPrice) as OPF FROM Orders;
  ```

  + MAX(col)/MIN(col)  返回某列的最大值/最小值

  ```
  SELECT MAX(column_name) FROM table_name
  查找 "OrderPrice" 列的最大值
  SELECT MAX(OrderPrice) as MOP FROM Orders;
  ```

  + SUM(col) 返回某列的总值
  + GROUP BY 用于结合合计函数，根据一个或多个列对结果进行分组

  ```
  SELECT column_name, aggregate_function(column_name)
  FROM table_name
  WHERE column_name operator value
  GROUP BY column_name
  查找每个客户的总金额
  SELECT Customer,SUM(OrderPrice) FROM Orders
  GROUP BY Customer；
  GROUP BY 一个以上的列
  SELECT Customer,OrderDate,SUM(OrderPrice) FROM Orders
  GROUP BY Customer,OrderDate;
  ```

  + HAVING 在 SQL 中增加 HAVING 子句原因是，WHERE 关键字无法与合计函数一起使用。

  ```
  SELECT column_name, aggregate_function(column_name)
  FROM table_name
  WHERE column_name operator value
  GROUP BY column_name
  HAVING aggregate_function(column_name) operator value;
  查找订单总金额少于 2000 的客户
  SELECT Customer,SUM(OrderPrice) FROM Orders
  GROUP BY Customer
  HAVING SUM(OrderPrice)<2000;
  查找客户 "Bush" 或 "Adams" 拥有超过 1500 的订单总金额
  SELECT Customer,SUM(OrderPrice) FROM Orders
  WHERE Customer='Bush' OR Customer='Adams'
  GROUP BY Customer
  HAVING SUM(OrderPrice)>1500;
  ```

  ​

+ scalar函数

  + UCASE(c) /LCASE(c) 将某个域转换为大写/小写

  ```
  SELECT UCASE(LastName) as LastName,FirstName FROM Persons
  ```

  + MID(c) 用于从文本字段中提取字符

  ```
  SELECT MID(column_name,start[,length]) FROM table_name
  从 "City" 列中提取前 3 个字符
  SELECT MID(City,1,3) as SmallCity FROM Persons;
  ```

  ​

  + LEN(c) 返回某个文本域的长度
  + ROUND(c,decimals) 对某个数值域进行指定小数位的四舍五入
  + FORMAT(c,format) 改变某个域的显示方式 



+ 数学函数 主要处理数字

![数学函数](http://img.blog.csdn.net/20160413143556761)

+ 字符串函数

![这里写图片描述](http://img.blog.csdn.net/20160413144023924)

+ 日期和时间函数

  ![这里写图片描述](http://img.blog.csdn.net/20160413150046684)

MySQL日期间隔类型如下

![这里写图片描述](http://img.blog.csdn.net/20160413150331240)

MySQL日期时间格式如下

![这里写图片描述](http://img.blog.csdn.net/20160413150427178)

![这里写图片描述](http://img.blog.csdn.net/20160413150455209)

+ 条件判读函数

  + if(expr,v1,v2) 如果表达式expr成立，返回结果v1，否则返回结果v2。

  - ifnull(v1,v2) 如果v1不为空，就显示v1的值，否则就显示v2的值。
  - case
    - case when exp1 then v1 [when exp2 then v2 ...]\[else vn] end 类似于if else
    - case expr when e1 then v1 [when e2 then v2]\[else vn] end 类似于case

  ## 









[简单实例理解主键与外键](http://www.aspku.com/database/mysql/79442.html)

[对外键的一些操作](https://www.cnblogs.com/zunpeng/p/3878459.html)

[mysql中的一些专业术语](http://www.cnblogs.com/DannyShi/p/4617469.html)

[mysql中的约束](http://blog.csdn.net/a909301740/article/details/62887992)

### Hbase篇

+ 打来工作环境 hbase shell
+ ​

