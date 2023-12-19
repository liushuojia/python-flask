# python-flask

## 简单web的研发，实现基础框架
    POST /user 创建一个用户
    GET /user 查询用户信息
    GET /user/:id 获取一个用户信息
    PUT /user/:id 更新一个用户信息
    DELETE /user/:id 删除一个用户

    缓存数据
    GET /cache/user 获取所有缓存用户， 如用户不存在则创建缓存
    GET /cache/user/:id 获取一个缓存用户
    

## 项目使用flask框架，DDD设计思想
    api 所有web RESTful api 函数

## 数据库使用mysql 使用 sqlalchemy
    对象使用DB.py基类，

## 缓存使用redis 
    其中python为解释型语言