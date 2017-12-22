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

    ---

  + drop table 表名；

  + 删除被关联的父表 应先删除子表的外键约束再删除父表

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

    ---

    + describe 表名；
    + show create table 表名；查看表的详细定义
    + show tables;

---









[简单实例理解主键与外键](http://www.aspku.com/database/mysql/79442.html)

[对外键的一些操作](https://www.cnblogs.com/zunpeng/p/3878459.html)

[mysql中的一些专业术语](http://www.cnblogs.com/DannyShi/p/4617469.html)

[mysql中的约束](http://blog.csdn.net/a909301740/article/details/62887992)

### Hbase篇

+ 打来工作环境 hbase shell
+ ​

