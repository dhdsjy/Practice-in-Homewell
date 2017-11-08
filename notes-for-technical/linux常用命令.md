# linux常用命令

## 写在前面

其实这个笔记在4月份准备春招考试的时候写过一次，然后window土著，很快就忘记了。。现在实习刚好一直在Ubuntu下，好好熟悉下吧，程序员的基本技能啊！



**root 权限切换**

+ 普通用户获取root权限
  + 非永久性获取 sudo
  + 永久性获取 sudo su 退出exit即可

## 文件处理命令

**mkdir** mkdir命令的作用是建立名称为dirname的子目录，它的使用权限是所有用户。格式：mkdir [options] 目录名 －m, －－mode=模式：设定权限<模式>，与chmod类似。

```
在进行目录创建时可以设置目录的权限，此时使用的参数是“－m”。假设要创建的目录名是“tsk”，让所有用户都有rwx(即读、写、执行的权限)，那么可以使用以下命令：
$ mkdir －m 777 tsk
```

**grep** Linux系统中grep命令是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹 配的行打印出来。grep全称是Global Regular Expression Print，表示全局正则表达式版本，它的使用权限是所有用户。格式：grep [options]

```
$ grep ‘test’ d*
显示所有以d开头的文件中包含 test的行。
$ grep ‘test’ aa bb cc
显示在aa，bb，cc文件中匹配test的行。
```

**find** find命令的作用是在目录中搜索文件，它的使用权限是所有用户。格式：find [path][options][expression]；path指定目录路径，系统从这里开始沿着目录树向下查找文件。它是一个路径列表，相互用空格分离，如果不写path，那么默认为当前目录。

```
（1）根据文件名查找
例如，我们想要查找一个文件名是lilo.conf的文件，可以使用如下命令：
find / －name lilo.conf
find命令后的“/”表示搜索整个硬盘。
(2) 根据部分文件名查找方法
有时我们知道只某个文件包含有abvd这4个字，那么要查找系统中所有包含有这4个字符的文件可以输入下面命令：
find / －name '*abvd*'
```

**cat** cat（“concatenate”的缩写）命令用于连接并显示指定的一个和多个文件的有关信息，它的使用权限是所有用户。

```
cat主要有三大功能：
1.一次显示整个文件。$ cat filename
2.从键盘创建一个文件。$ cat > filename  这个用touch比较多
   只能创建新文件,不能编辑已有文件.
3.将几个文件合并为一个文件： $cat file1 file2 > file
```

**history**