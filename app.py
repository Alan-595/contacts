from flask import Flask, render_template, request, redirect, url_for, flash  # 导入Flask模块用于构建Web应用
import pymysql.cursors  # 导入pymysql模块以连接和操作MySQL数据库

# Connect to the database
connection = pymysql.connect(host='localhost',  # 数据库主机地址
                             user='root',  # 数据库用户名
                             password='123456',  # 数据库密码
                             db='user_test',  # 要连接的数据库名称
                             charset='utf8mb4',  # 设置字符集，支持中文字符
                             cursorclass=pymysql.cursors.DictCursor)  # 设置游标类型，使结果以字典格式返回

app = Flask(__name__)  # 初始化Flask应用

# 保持数据库连接
def getconnection():
    connection.ping(reconnect=True)  # 保持数据库连接，如果断开则重新连接
    return connection  # 返回数据库连接

# 首页
@app.route('/')  # 定义根路径的路由，即主页
def index():
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "SELECT * FROM `tb_user`"  # 定义SQL查询语句
            cols = ['id', 'name', 'gender', 'age', 'phone']  # 设置要显示的列名
            cursor.execute(sql)  # 执行查询
            result = cursor.fetchall()  # 获取查询结果
            cursor.close()  # 关闭游标
            return render_template("index.html", items=result, cols=cols, success='')  # 渲染index.html模板，并传递查询结果
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("index.html", items=[], cols=[], success='Can\'t view index: ' + str(e))  # 如果出错，返回空数据和错误信息

# 搜索
@app.route('/search')  # 定义搜索路径的路由
def search():
    keyword = request.args.get('keyword').strip()  # 从请求中获取关键词并去掉首尾空格
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "SELECT * FROM `tb_user` where name like concat('%%',%s,'%%')"  # 定义SQL查询语句，模糊查询名字
            cols = ['id', 'name', 'gender', 'age', 'phone']  # 设置要显示的列名
            cursor.execute(sql, (keyword))  # 执行查询，传入关键词
            result = cursor.fetchall()  # 获取查询结果
            cursor.close()  # 关闭游标
            return render_template("index.html", items=result, keyword=keyword, cols=cols, success='')  # 渲染index.html模板，并传递查询结果
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("index.html", items=[], cols=[], success='search error: ' + str(e))  # 如果出错，返回空数据和错误信息

# 跳转到新增页面
@app.route('/toAddPage')  # 定义跳转到新增页面的路由
def toAddPage():
    return render_template('add.html')  # 渲染add.html模板

# 跳转到编辑页面
@app.route('/toEditPage/<int:id>')  # 定义编辑页面的路由，接收用户ID
def toEditPage(id):
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "select * from `tb_user` where id=%s"  # 定义SQL查询语句，按ID查找用户
            cursor.execute(sql, (id))  # 执行查询，传入用户ID
            result = cursor.fetchone()  # 获取查询结果（单个用户信息）
            cursor.close()  # 关闭游标
            return render_template("edit.html", item=result, success='')  # 渲染edit.html模板，并传递用户信息
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))  # 如果出错，返回错误信息

# 新增用户
@app.route('/add', methods=['POST'])  # 定义新增用户的路由，仅接受POST请求
def add():
    name = request.form['name'].strip()  # 获取表单中的用户名并去掉首尾空格
    age = request.form['age'].strip()  # 获取表单中的年龄并去掉首尾空格
    gender = request.form['gender'].strip()  # 获取表单中的性别并去掉首尾空格
    phone = request.form['phone'].strip()  # 获取表单中的联系方式并去掉首尾空格
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "INSERT INTO `tb_user` (`name`, `age`, `gender`, `phone`) VALUES (%s, %s, %s, %s)"  # 定义插入用户信息的SQL语句
            cursor.execute(sql, (name, age, gender, phone))  # 执行插入语句，传入用户信息
            cursor.close()  # 关闭游标
            return redirect(url_for("index"))  # 重定向到首页
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("add.html", success='Can\'t add User: ' + str(e))  # 如果出错，返回错误信息并渲染add.html页面

# 编辑用户
@app.route('/edit', methods=['POST'])  # 定义编辑用户的路由，仅接受POST请求
def edit():
    id = request.form['id'].strip()  # 获取表单中的用户ID并去掉首尾空格
    name = request.form['name'].strip()  # 获取表单中的用户名并去掉首尾空格
    age = request.form['age'].strip()  # 获取表单中的年龄并去掉首尾空格
    phone = request.form['phone'].strip()  # 获取表单中的联系方式并去掉首尾空格
    gender = request.form['gender'].strip()  # 获取表单中的性别并去掉首尾空格
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "update `tb_user` set name=%s, age=%s, gender=%s, phone=%s where id=%s"  # 定义更新用户信息的SQL语句
            cursor.execute(sql, (name, age, gender, phone, id))  # 执行更新语句，传入用户信息和ID
            cursor.close()  # 关闭游标
            return redirect(url_for("index"))  # 重定向到首页
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))  # 如果出错，返回错误信息并渲染edit.html页面

# 删除用户
@app.route('/remove/<int:id>/')  # 定义删除用户的路由，接收用户ID
def remove(id):
    try:
        with getconnection().cursor() as cursor:  # 获取数据库连接的游标
            sql = "delete from `tb_user` where id=%s"  # 定义删除用户的SQL语句
            cursor.execute(sql, (id))  # 执行删除语句，传入用户ID
            cursor.close()  # 关闭游标
            return redirect(url_for("index"))  # 重定向到首页
    except Exception as e:  # 处理异常
        cursor.close()  # 关闭游标
        return render_template("index.html", success='Can\'t remove User: ' + str(e))  # 如果出错，返回错误信息并渲染index.html页面

# 处理404错误
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404  # 渲染404错误页面并返回状态码404

# 处理500错误
@app.errorhandler(500)
def system_error(error):
    return render_template('500.html'), 500  # 渲染500错误页面并返回状态码500

# 启动应用
if __name__ == '__main__':
    app.jinja_env.auto_reload = True  # 设置模板自动重新加载
    app.run(host='127.0.0.1', port=8001, debug=True)  # 启动Flask应用，监听本地8001端口，启用调试模式
