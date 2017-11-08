# MySQL&JavaScript

## 写在前面

MySQL主要掌握的是sql查询语句，而且常用的也就那么20+条，作为一个数据分析人员，没必要掌握的那么深。先掌握这最基本且常用的20%，IT领域是一个不断学习的过程，想一次性整个的学完，不现实，时间一长也就忘了。

2017.11.06 MySQL的学习，看的比较系统.udacity讲座，一般般

2017.11.07 重点学习MySQL的查询语句、Hbase

## SQL常用查询语句

### 查

+ DESCRIBE TableName; 查看表结构

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

  + WHERE 查询指定记录 
    + BETWEEN AND 、NOT BETWEEN AND 指定范围(包含等于)   XX [NOT] BETWEEN 取值1 AND 取值2
    + IN、NOT IN 指定集合       XX [NOT] IN (元素1，元素2，...，元素n)
    + LIKE、NOT LIKE 匹配字符 XX [NOT] LIKE '字符串' %表示任意个字符，_表示一个字符，一个汉字是两个字符哦
    + IS NULL、IS NOT NULL是否为空值 XX IS [NOT] NULL
    + AND、OR 多个查询条件  条件表达式1 AND/OR 条件表达式2 [...AND/OR条件表达式n]

+ 连接查询 将多个表按某个条件连接起来，从中选择需要的数据

  + 内连接查询 最常用的连接查询方式，通常将两张表中具有相同意义的字段进行值相等相连

    ```
    select b.*,a.* from organization as b,entity as a
    where b.id = a.orgid limit 1000;

    select s.name,m.mark from student s inner join mark m on s.id=m.studentid
    ```

  + 外连接查询 不仅可以查询出该字段取值相同的记录，也可以查询出该字段取值不相等时的记录，分为左连接和右连接 参数on后面就是连接条件，进行左连接查询时，可以查询出表名1中的所有记录，而表名2中只能查询出匹配的记录

    ```
    # 左连接 将左边的字段全部选出来 所以连接后的记录条数大于等于连接前的条数
    select s.name,m.mark from student s left join mark m on s.id=m.studentid
    # 右连接 右连接就是把右边表的数据全部取出，不管左边的表是否有匹配的数据
    select s.name,m.mark from student s right join mark m on s.id=m.studentid
    # 全连接 把左右两个表的数据都取出来，不管是否匹配
    select s.name,m.mark from student s full join mark m on s.id=m.studentid

    ```

+ 子查询 子查询是将一个查询语句嵌套在另一个查询语句中，即实现多表之间的查询。内层查询语句的查询结果，为外层查询语句提供查询条件。

  + 带比较运算符的子查询 

    ```
    select d_id,d_name from department
    where d_id != 
    (select d_id from employee where age=24)
    ```

  + 综合查询

  ```
  select * from organization as b
  left join
  (select * from entity where id = 1) as a
  on b.id = a.orgid
  ```

+ 合并查询结果 将多个select语句查询结果合并到一起显示；使用UNION时，数据库系统会将所有的查询结果合并到一起然后去除掉相同的记录，类似于进行集合；而使用UNION ALL时，只是将所有查询结果进行简单合并，并不剔除相同的记录。

+ 使用正则表达式查询

  ![正则表达式](http://img.blog.csdn.net/20160413093748539)

### 改

+ 修改表 修改表名、数据类型、字段名、增加/删除字段、修改字段排列位置、更改默认存储引擎、删除表的外键约束
  + 修改表名 alter table 旧表名 rename [to] 新表名
  + 修改字段名 alter table 表名 change 旧属性名 新属性名 新数据类型
  + 修改字段数据类型 alter table 表名 modify 属性名 新数据类型
  + 增加字段 alter table 表名 add 属性名1 数据类型[完整性约束]/[ firest|after 属性名2]
  + 删除字段 alter table 表名 drop 属性名；
  + 删除表的外键约束 alter table 表名 drop foreign key 外键别名


+ 更新数据 更新数据即更新表中已经存在的记录，可以改变表中已经存在的数据。基本语法为

  ```
  update 表名
  set 属性名1=取值1，属性名2=取值2,...,属性名n=取值n
  WHERE 条件表达式； /指定更新满足条件的记录，即要跟新的目标记录
  ```

### 增

+ 插入数据

  + 向表中所有字段插入数据

    ```
    # 方法一
    insert into 表名 values（值1，值2，...,值n） /注意顺序和字段数据类型一致
    # 方法二 该方法还可以想表中指定字段插入数据
    insert into 表名（属性1，属性2，...,属性m）
    values（值1，值2，...,值m）
    ```

  + 同时插入多条记录

    ```
    insert into 表名 [(属性列表)] values (取值列表1)，(取值列表2),...,(取值列表m);
    ```

  + 将查询结果插入表中

    ```
    insert into 表名1 (属性列表1) select 属性列表1 from 表名2 where 条件表达式 
    ```

### 删

+ 删除表

  + 删除没有被关联的普通表

    ```
    drop table 表名
    ```

  + 删除被关联的父表

    + 先删除与之关联的子表，再删除父表
    + 先删除子表的外键约束，再删除父表[推荐]


+ 删除数据 删除数据即删除表中已经存在的记录，可以删除表中不再使用的数据。基本语法为

  ```
  delete from 表名 [WHERE 条件表达式]
  ```

  where用来指定待删除的目标记录，如果没有条件表达式，数据库系统就会删除表中的所有数据。 

  注意，系统对删除过程不会有任何提示，所以要谨慎。

### SQL常用内部函数

丰富的函数可以简化用户的操作，让操作更加灵活，此外，由于函数的执行速度非常快，还可以提高MySQL的处理速度。 前面介绍到的Select语句及其条件表达式，Insert、Update和Delete语句及其条件表达式都可以使用这些函数。 MySQL函数包括数学函数、字符串函数、日期和时间函数、条件判断函数、徐彤信息函数、加密函数、格式化函数等。下面将详细介绍这些函数的使用方法。

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

+ 条件判断函数
  + if(expr,v1,v2) 如果表达式expr成立，返回结果v1，否则返回结果v2。
  + ifnull(v1,v2) 如果v1不为空，就显示v1的值，否则就显示v2的值。
  + case
    + case when exp1 then v1 [when exp2 then v2 ...]\[else vn] end 类似于if else
    + case expr when e1 then v1 [when e2 then v2]\[else vn] end 类似于case

## 参考链接

[sql中的连接查询](http://www.cnblogs.com/still-windows7/archive/2012/10/22/2734613.html)

[SQL查询](http://blog.csdn.net/lipengcn/article/details/51133516)

