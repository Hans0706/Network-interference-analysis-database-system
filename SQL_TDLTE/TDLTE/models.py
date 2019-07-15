import pymssql

# 数据库远程连接
my_db = pymssql.connect(host="10.28.225.209", user="sa", password="jihuxiao", database="TD_LTE", charset="utf8")
#my_db = pymssql.connect(host="10.128.255.54", user="sa", password="Tobias=4", database="SMBar0415", charset="utf8")
# cursor = conn.cursor()
# #游标激活触发器
# cursor.execute('SELECT * FROM tbCell')
# print( cursor.fetchall() )  # 显示出的是c2游标查询出来的结果
# print('ss')