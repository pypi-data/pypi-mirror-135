# postgresql_kernel

+ author: hsz12
+ author-email: hsz1273327@gmail.com

keywords: jupyter,jupyter-kernel,postgresql,sql

本项目fork自[postgres_kernel](https://github.com/bgschiller/postgres_kernel).由于这个项目已经快4年每更新过了而我自己常用它,但它又有一些不好用的地方所以才有了现在这个项目.

## 特性

+ 输入sql语言获得表格结果
+ 可选的自动提交
+ 不再需要设置环境变量`DATABASE_URL`
+ jupyter console中可以退出.

## TODO

1. 加入常用可视化功能
2. 改用魔术命令配置连接信息

<!-- ## 安装

`pip install postgresql_kernel` -->

## 使用

1. 连接设置

    ```sql
    -- connection: postgres://postgres:postgres@localhost:5432/postgres
    -- autocommit: true
    -- (or false)
    ```

2. 输入sql获得结果
-- connection: postgres://postgres:postgres@localhost:5433/postgres