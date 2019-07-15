# Create your views here.
import jsonresponse
from django.shortcuts import render

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime
import pymssql
import xlrd
import csv
import xlwt
from django.http import JsonResponse

#主页
from TDLTE.form import *
from TDLTE.models import my_db
from TDLTE.math import *
import re

def index(request):
    return render(request,'index.html',locals())

def main(request):
    return render(request,'main.html',locals())

global nrows
global i
#登录
def login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            cursor = my_db.cursor(as_dict=True)
            cursor.execute("select password from Users where username=%s", username)
            pw = cursor.fetchall()
            if pw[0]['password'] == password:
                return render(request, 'main.html')
            else:
                return render(request, 'error.html', {'reason': '密码或用户名不正确'})
        else:  # GET方法，如第一次进入登陆页面
            login_form = LoginForm()
            return render(request, 'main.html')
    except Exception as e:
        return render(request, 'error.html', {'reason': '密码或用户名不正确'})
        pass




def regist(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            # if reg_form.is_valid():  # 校验表单
            username = request.POST["username"]
            password = request.POST["password"]
            cs=my_db.cursor(as_dict=True)
            cs.execute('select username from Users')
            un=cs.fetchall()
            if username in un:
                print("用户名重复")#todo 弹窗
                return render(request,'index.html',locals())
            else:
                cursor=my_db.cursor()
                cursor.execute('insert into Users values(%s,%s)',(username,password))
            # 注册后直接登录
                my_db.commit()
                return render(request, 'main.html', locals())
        else:
            reg_form = RegForm()
    except Exception as e:
        print("ERROR!")
        return render(request,'error.html')
        pass





#退出 todo html
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        pass
    return render(request, 'index.html', locals())



#数据库操作

#导入数据
def import_data(request):
    global nrows
    global i
    nrows=1
    i=0
    try:
        if request.method == 'POST':
            imp_Form = ImportForm(request.POST,request.FILES)
            partition=int(request.POST['partition'])
            if request.POST['file_type'] == '.xls,.xlsx':
                wb = xlrd.open_workbook(file_contents=request.FILES.get('file_name').read())
                table=wb.sheets()[0]
                nrows=table.nrows
                if request.POST['table'] == 'MROData':
                    current=1
                    while i < table.nrows:
                        stmt = "insert into tbMROData values"
                        j=0
                        while j <partition and i<table.nrows:
                            row = table.row_values(i)
                            if row[5] == 37900 or row [5] == 38098 or row [5] == 38400 or row [5] == 38496 or row [5] == 38544 or row [5] == 38950 or row [5] == 39148:
                                stmt+='('+str(row[0])+',\''+row[1]+'\',\''+row[3]+'\','+str(row[4])+','+str(row[5])+','+str(row[6])+','+str(row[7])+'),'
                                j+=1
                            i+=1
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'Cell':
                    i=1
                    while i < table.nrows:
                        stmt = "insert into tbCell values"
                        j=0
                        while j <partition and i<table.nrows:
                            row = table.row_values(i)
                            if (row[5] == 37900 or row [5] == 38098 or row [5] == 38400 or row [5] == 38496 or row [5] == 38544 or row [5] == 38950 or row [5] == 39148) and row[6] >= 0 and row[6] <= 503 and row[6] == row[7] + row[8] * 3 and (row[10] == '华为' or row[10] == '中兴' or row[10] == '诺西' or row[10] == '爱立信' or row[10] == '贝尔' or row[10] == '大唐') and row[11] >= -180 and row[11] <= 180 and row[12] >= -90 and row[12] <= 90 and (row[13] == '室分' or row[13] == '宏站') and row[18] == row[17] + row[16] and row[15]!='隧道内':
                                stmt+='(\''+row[0]+'\',\''+row[1]+'\',\''+row[2]+'\','+str(row[3])+',\''+row[4]+'\','+str(row[5])+','+str(row[6])+','+str(row[7])+','+str(row[8])+','+str(row[9])+',\''+row[10]+'\','+str(row[11])+','+str(row[12])+',\''+row[13]+'\',0'+str(row[14])+',0'+str(row[15])+',0'+str(row[16])+',0'+str(row[17])+',0'+str(row[18])+'),'
                                j+=1
                            i+=1
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'PRB':
                    i=1
                    while i < table.nrows:
                        stmt = "insert into tbPRB values"
                        j=0
                        while j <50 and i<table.nrows:
                            row = table.row_values(i)
                            stmt+='(\''+str(row[0])+'\',\''+row[2]+'\',\''+row[4]+'\',\''+row[3]+'\','
                            for k in range(5,104):
                                if str(row[k])!='NIL':
                                    stmt+=str(row[k])+','
                                else:
                                    stmt+='NULL,'
                            stmt+=str(row[104])+'),'
                            j+=1
                            i+=1
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'KPI':
                    flag=0
                    if flag==0:
                        i=1
                        while i < table.nrows:
                            stmt = "insert into tbKPI values"
                            j=0
                            while j <partition and i<table.nrows:
                                row = table.row_values(i)
                                stmt+='(\''+str(row[0])+'\',\''+row[2]+'\',\''+row[4]+'\',\''+row[3]+'\','
                                for k in range(5,41):
                                    if str(row[k])!='NIL':
                                        stmt+=str(row[k])+','
                                    else:
                                        stmt+='NULL,'
                                stmt+=str(row[41])+'),'
                                j+=1
                                i+=1
                            stmt=stmt[:-1]
                            cursor=my_db.cursor()
                            cursor.execute(stmt)
                            #cursor.executemany(stmt)
                            my_db.commit()
                    else:
                        cursor=my_db.cursor()
                        cursor.execute("bulk insert tbKPI from 'C:\\Users\\电竞林俊杰\\Desktop\\表12优化区17日-19日KPI指标统计表-0717至0719.xls' with batchsize="+str(partition)+",fire_triggers")
                        my_db.commit()

            elif request.POST['file_type'] == '.csv':
                file=request.FILES.get('file_name')
                data=file.read().decode('utf-8')
                lines=data.split('\r\n')
                nrows=len(lines)
                if request.POST['table'] == 'MROData':
                    i=3
                    j=0
                    flag=1
                    for line in lines:
                        if flag==1:
                            flag=0
                        else:
                            i+=1
                            row=line.split(',')
                            if j==0:
                                stmt = "insert into tbMROData values"
                            if len(row)>1:
                                if row[6] == '37900' or row [6] == '38098' or row [6] == '38400' or row [6] == '38496' or row [6] == '38544' or row [6] == '38950' or row [6] == '39148':
                                    stmt+='('+str(row[0])+',\''+row[1]+'\',\''+row[2]+'\',\''+row[3]+'\','+str(row[4])+','+str(row[5])+','+str(row[6])+','+str(row[7])+'),'
                                    j+=1
                            if j==partition:
                                stmt=stmt[:-1]
                                cursor=my_db.cursor()
                                cursor.execute(stmt)
                                my_db.commit()
                                j=0
                    if j!=0:
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'Cell':
                    j=0
                    i=3
                    flag=1
                    for row in data:
                        if flag==1:
                            flag=0
                        else:
                            i+=1
                            if j==0:
                                stmt = "insert into tbCell values("
                            if (row[5] == 37900 or row [5] == 38098 or row [5] == 38400 or row [5] == 38496 or row [5] == 38544 or row [5] == 38950 or row [5] == 39148) and row[6] >= 0 and row[6] <= 503 and row[6] == row[7] + row[8] * 3 and (row[10] == '华为' or row[10] == '中兴' or row[10] == '诺西' or row[10] == '爱立信' or row[10] == '贝尔' or row[10] == '大唐') and row[11] >= -180 and row[11] <= 180 and row[12] >= -90 and row[12] <= 90 and (row[13] == '室分' or row[13] == '宏站') and row[18] == row[17] + row[16]:
                                stmt+='(\''+row[0]+'\',\''+row[1]+'\',\''+row[2]+'\',\''+row[3]+'\',\''+row[4]+'\','+str(row[5])+','+str(row[6])+','+str(row[7])+','+str(row[8])+','+str(row[9])+',\''+row[10]+'\','+str(row[11])+','+str(row[12])+',\''+row[13]+'\','+str(row[14])+','+str(row[15])+','+str(row[16])+','+str(row[17])+','+str(row[18])+'),'
                                j+=1
                            if j==partition:
                                stmt=stmt[:-1]
                                stmt+=')'
                                cursor=my_db.cursor()
                                cursor.execute(stmt)
                                my_db.commit()
                                j=0
                    if j!=0:
                        stmt=stmt[:-1]
                        stmt+=')'
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'PRB':
                    j=0
                    i=3
                    flag=1
                    for row in data:
                        if flag==1:
                            flag=0
                        else:
                            i+=1
                            if j==0:
                                stmt = "insert into tbPRB values"
                            stmt+='(\''+str(row[0])+'\',\''+row[2]+'\',\''+row[4]+'\',\''+row[3]+'\','
                            for k in range(5,104):
                                if str(row[k])!='NIL':
                                    stmt+=str(row[k])+','
                                else:
                                    stmt+='NULL,'
                            stmt+=str(row[104])+'),'
                            j+=1
                            if j==partition:
                                stmt=stmt[:-1]
                                stmt+=')'
                                cursor=my_db.cursor()
                                cursor.execute(stmt)
                                my_db.commit()
                                j=0
                    if j!=0:
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
                elif request.POST['table'] == 'KPI':
                    j=0
                    i=3
                    flag=1
                    for row in data:
                        if flag==1:
                            flag=0
                        else:
                            i+=1
                            if j==0:
                                stmt = "insert into tbKPI values"
                            stmt+='(\''+str(row[0])+'\',\''+row[2]+'\',\''+row[4]+'\',\''+row[3]+'\','
                            for k in range(5,41):
                                if str(row[k])!='NIL':
                                    stmt+=str(row[k])+','
                                else:
                                    stmt+='NULL,'
                            stmt=stmt[:-1]
                            stmt+='),'
                            j+=1
                            if j== partition:
                                stmt=stmt[:-1]
                                stmt+=')'
                                cursor=my_db.cursor()
                                cursor.execute(stmt)
                                my_db.commit()
                                j=0
                    if j!=0:
                        stmt=stmt[:-1]
                        cursor=my_db.cursor()
                        cursor.execute(stmt)
                        my_db.commit()
            # todo ？ return HttpResponse("ok")
        else:
            imp_Form = ImportForm()
    except Exception as e:
        print(e.args)
        pass
    return render(request, 'loadData.html', locals())

def get_progress(request):
    global i
    global nrows
    print(i/nrows)
    return JsonResponse(100*i/nrows, safe=False)

#导出数据
def export_data(request):
    if request.method=='POST':
        if request.POST['table']=='tbCell':
            path=request.POST['route']
            path=path.replace("\\","/")
            path=path+'/tbCell.xls'
            cursor1 = my_db.cursor()
            cursor1.execute('select * from tbCell')
            CELL=cursor1.fetchall()
            fields=cursor1.description
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建Excel中的一个sheet，并命名且为可重写状态。
            sheet = workbook.add_sheet('result_count', cell_overwrite_ok=True)
            # 构造一个列表VnameList，用于将上述表头重命名，一定要一一对应。
            VnameList = ['CITY', 'SECTOR_ID', 'SECTOR_NAME', 'ENODEBID', 'ENODEB_NAME', 'EARFCN', 'PCI', 'PSS', 'SSS',
                         'TAC', 'VENDOR', 'LONGITUDE', 'LATITUDE', 'STYLE', 'AZIMUTH', 'HEIGHT', 'ELECTTILT',
                         'MECHTILT', 'TOTLETILT']
            # 将上述list中的虚拟身份依次填入Excel中去。
            for field in range(0, len(VnameList)):
                # sheet.write(0,field,fields[field][0])
                sheet.write(0, field, VnameList[field])

            # 根据横纵坐标依次录入查询到的信息值。
            row = 1
            col = 0
            for row in range(1, len(CELL) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % CELL[row - 1][col])
            # 格式化时间输出，用于给Excel起名时使用。
            sheet_time = datetime.datetime.now()
            book_mark = sheet_time.strftime('%Y%m%d')
            workbook.save(path)
            my_db.commit()
            return render(request, 'exportData.html', {'info': "Success!"})
        if request.POST['table']=='KPI':
            path = request.POST['route']
            path = path.replace("\\", "/")
            path = path + '/tbKPI.xls'
            cursor1 = my_db.cursor()
            cursor1.execute('select * from tbKPI')
            KPI=cursor1.fetchall()
            fields = cursor1.description
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建Excel中的一个sheet，并命名且为可重写状态。
            sheet = workbook.add_sheet('result_count', cell_overwrite_ok=True)
            # 构造一个列表VnameList，用于将上述表头重命名，一定要一一对应。
            VnameList = [u'起始时间',	'周期',	'网元名称',	'小区',	'小区',	'RRC连接建立完成次数 (无)',	'RRC连接请求次数（包括重发） (无)',	'RRC建立成功率qf (%)',
                         'E-RAB建立成功总次数 (无)',	'E-RAB建立尝试总次数 (无)',	'E-RAB建立成功率2 (%)',	'eNodeB触发的E-RAB异常释放总次数 (无)',	'小区切换出E-RAB异常释放总次数 (无)',
                         'E-RAB掉线率(新) (%)',	'无线接通率ay (%)',	'eNodeB发起的S1 RESET导致的UE Context释放次数 (无)',	'UE Context异常释放次数 (无)',	'UE Context建立成功总次数 (无)',
                         '无线掉线率 (%)',	'eNodeB内异频切换出成功次数 (无)',	'eNodeB内异频切换出尝试次数 (无)',	'eNodeB内同频切换出成功次数 (无)',	'eNodeB内同频切换出尝试次数 (无)',
                         'eNodeB间异频切换出成功次数 (无)',	'eNodeB间异频切换出尝试次数 (无)',	'eNodeB间同频切换出成功次数 (无)',	'eNodeB间同频切换出尝试次数 (无)',	'eNB内切换成功率 (%)',
                         'eNB间切换成功率 (%)',	'同频切换成功率zsp (%)',	'异频切换成功率zsp (%)',	'切换成功率 (%)',	'小区PDCP层所接收到的上行数据的总吞吐量 (比特)',	'小区PDCP层所发送的下行数据的总吞吐量 (比特)',
                         'RRC重建请求次数 (无)',	'RRC连接重建比率 (%)',	'通过重建回源小区的eNodeB间同频切换出执行成功次数 (无)',	'通过重建回源小区的eNodeB间异频切换出执行成功次数 (无)',	'通过重建回源小区的eNodeB内同频切换出执行成功次数 (无)',
                         '通过重建回源小区的eNodeB内异频切换出执行成功次数 (无)',	'eNB内切换出成功次数 (次)',	'eNB内切换出请求次数 (次)']

            # 将上述list中的虚拟身份依次填入Excel中去。
            for field in range(0, len(VnameList)):
                # sheet.write(0,field,fields[field][0])
                sheet.write(0, field, VnameList[field])

            # 根据横纵坐标依次录入查询到的信息值。
            row = 1
            col = 0
            for row in range(1, len(KPI) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % KPI[row - 1][col])
            workbook.save(path)
            my_db.commit()
            return render(request, 'exportData.html', {'info': "Success!"})
            #导出数据
        if request.POST['table']=='PRB':
            path = request.POST['route']
            path = path.replace("\\", "/")
            path = path + '/tbPRB.txt'
            f = open(path, "w+")
            cursor1 = my_db.cursor()
            cursor1.execute('select * from tbPRB')
            PRB=cursor1.fetchall()
            fields = cursor1.description
            VnameList = ['STARTTIME',
                         'ENODEB_NAME',
                         'SECTOR_NAME',
                         'REMARKS', 'AVG_0', 'AVG_1', 'AVG_2', 'AVG_3', 'AVG_4', 'AVG_5', 'AVG_6', 'AVG_7', 'AVG_8',
                         'AVG_9',
                         'AVG_10', 'AVG_11', 'AVG_12', 'AVG_13', 'AVG_14', 'AVG_15', 'AVG_16', 'AVG_17', 'AVG_18',
                         'AVG_19',
                         'AVG_20', 'AVG_21', 'AVG_22', 'AVG_23', 'AVG_24', 'AVG_25', 'AVG_26', 'AVG_27', 'AVG_28',
                         'AVG_29',
                         'AVG_30', 'AVG_31', 'AVG_32', 'AVG_33', 'AVG_34', 'AVG_35', 'AVG_36', 'AVG_37', 'AVG_38',
                         'AVG_39',
                         'AVG_40', 'AVG_41', 'AVG_42', 'AVG_43', 'AVG_44', 'AVG_45', 'AVG_46', 'AVG_47', 'AVG_48',
                         'AVG_49',
                         'AVG_50', 'AVG_51', 'AVG_52', 'AVG_53', 'AVG_54', 'AVG_55', 'AVG_56', 'AVG_57', 'AVG_58',
                         'AVG_59'
                         'AVG_60', 'AVG_61', 'AVG_62', 'AVG_63', 'AVG_64', 'AVG_65', 'AVG_66', 'AVG_67', 'AVG_68',
                         'AVG_69',
                         'AVG_70', 'AVG_71', 'AVG_72', 'AVG_73', 'AVG_74', 'AVG_75', 'AVG_76', 'AVG_77', 'AVG_78',
                         'AVG_79',
                         'AVG_80', 'AVG_81', 'AVG_82', 'AVG_83', 'AVG_84', 'AVG_85', 'AVG_86', 'AVG_87', 'AVG_88',
                         'AVG_89',
                         'AVG_90', 'AVG_91', 'AVG_92', 'AVG_93', 'AVG_94', 'AVG_95', 'AVG_96', 'AVG_97', 'AVG_98',
                         'AVG_99',
                         ]
            for field in range(0, len(VnameList)):
                f.write(VnameList[field])
                f.write('   ')

            for row in range(len(PRB)):
                f.write(str(PRB[row]))
                f.write('   ')
            f.close()
            my_db.commit()
            return render(request, 'exportData.html', {'info': "Success!"})

        if request.POST['table']=='tbMRO':
            path = request.POST['route']
            path = path.replace("\\", "/")
            path = path + '/tbMROData.txt'
            f=open(path,"w+")
            cursor1 = my_db.cursor()
            cursor1.execute('select * from tbMROData')
            MRO=cursor1.fetchall()
            fields = cursor1.description
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建Excel中的一个sheet，并命名且为可重写状态。
            sheet = workbook.add_sheet('result_count', cell_overwrite_ok=True)
            # 构造一个列表VnameList，用于将上述表头重命名，一定要一一对应。
            VnameList = ['TimeStamp',
            'ServingSector',
            'InterferingSector',
            'LteScRSRP',
            'LteNcRSRP',
            'LteNcEarfcn',
            'LteNcPci']

            # 将上述list中的虚拟身份依次填入Excel中去。
            for field in range(0, len(VnameList)):
                # sheet.write(0,field,fields[field][0])
                f.write("TimeStamp, ServingSector,  InterferingSector,  LteScRSRP,  LteNcRSRP,  LteNcEarfcn,    LteNcPci")

            # 根据横纵坐标依次录入查询到的信息值。

            for row in range(len(MRO)):
                f.write(str(MRO[row]))
                f.write('   ')
            f.close()
            my_db.commit()
            return render(request, 'exportData.html', {'info': "Success!"})
            # writer = csv.writer()



#查询界面跳转
def search_page00(request):
    return render(request,'loadData.html',locals())

def search_page01(request):
    return render(request,'exportData.html',locals())

def search_page08(request):
    return render(request, 'main.html', locals())

def search_page1(request):
    return render(request,'search1.html',locals())

def search_page2(request):
    return render(request,'search2.html',locals())


def search_page3(request):
    return render(request,'search3.html',locals())


def search_page4(request):
    return render(request,'search4_1.html',locals())

def search_page4_2(request):
    return render(request,'search4_2.html')

def search_page5(request):
    return render(request,'analyz.html',locals())

def search_page6(request):
    return render(request,'interrupt.html',locals())


#查询DB
#在tbCell里面查询
#根据sector查询小区信息
def search_data_1(request):
    zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    if request.POST:
        print('posting')
        attri=request.POST.get('attribute',None)

        cursor=my_db.cursor(as_dict=True)
        re.match=zhmodel.search(str(attri))

        if re.match:
            cursor.execute('select * from tbCell where SECTOR_NAME = %s',attri)
            data=cursor.fetchall()
            return render(request,'search1.html',{'info':data})
        else :
            #cursor.execute('select * from tbCell')
            cursor.execute('select * from tbCell where SECTOR_ID = %s',attri)
            data=cursor.fetchall()

            print(data)
            return render(request, 'search1.html', {'info': data})   #todo html接口

#根据enodeb查询小区信息
def search_data_2(request):
    zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    if request.POST:
        print('posting')
        attri = request.POST.get('attribute', None)

        cursor = my_db.cursor(as_dict=True)
        re.match = zhmodel.search(attri)
        if re.match:
            cursor.execute('select * from tbCell where ENODEB_NAME = %s', attri)
            data = cursor.fetchall()
            return render(request, 'search2.html', {'info': data})
        else:
            if str.isdigit(attri):
                cursor.execute('select * from tbCell where ENODEB_ID = %s', attri)
                data = cursor.fetchall()
                return render(request, 'search2.html', {'info': data})  # todo html接口
            #错误处理
            else:
                return render(request,'error.html')
def search_data_3(request):
    # todo 加界面提醒 查询2016年情况//表格横坐标大小减小?

    #搜索KPI画折线图
    date=['']*12
    attribute=['']*12
    if request.POST:
        print('posting')
        name = request.POST.get('name', None)
        attri = request.POST.get('attribute', None)
        start=request.POST.get('start',None)
        end=request.POST.get('end',None)


        start=start+(' 00:00:00')
        start=datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
        start=start.strftime('%m/%d/%Y %H:%M:%S')
        end=end+(' 00:00:00')
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        end = end.strftime('%m/%d/%Y %H:%M:%S')
        cursor = my_db.cursor(as_dict=True)
        cursor.execute('select *  from tbKPI where ENODEB_NAME= %s and STARTTIME between %s and %s ',(name,start,end))
        #cursor.execute('select *  from tbKPI ')
        data = cursor.fetchall()
        print(len(data))
        for i in range(len(data)):
            date[i]=data[i]['STARTTIME']
            attribute[i]=data[i][attri]
        print(date,attribute)
        return render(request, 'search3.html', {"info1":date,"info2":attribute})

def search_data_4_1(request):
    if request.method=='POST':
        path=request.POST['route']
        path = path.replace("\\", "/")
        path=path+'/tbPRBnew.txt'
        f = open(path, "w+")
        cursor = my_db.cursor()
        cursor1 = my_db.cursor()
        cursor1.execute('delete from tbPRBnew')
        my_db.commit()
        cursor.execute('exec hourly_PRB')
        my_db.commit()
        cursor2=my_db.cursor()
        cursor2.execute('select * from tbPRBnew')
        data=cursor2.fetchall()
        fields = cursor2.description
        VnameList = ['STARTTIME',
                     'ENODEB_NAME',
                     'SECTOR_NAME',
                     'REMARKS','AVG_0','AVG_1','AVG_2','AVG_3','AVG_4','AVG_5','AVG_6','AVG_7','AVG_8','AVG_9',
                     'AVG_10','AVG_11','AVG_12','AVG_13','AVG_14','AVG_15','AVG_16','AVG_17','AVG_18','AVG_19',
                     'AVG_20','AVG_21','AVG_22','AVG_23','AVG_24','AVG_25','AVG_26','AVG_27','AVG_28','AVG_29',
                     'AVG_30','AVG_31','AVG_32','AVG_33','AVG_34','AVG_35','AVG_36','AVG_37','AVG_38','AVG_39',
                     'AVG_40', 'AVG_41', 'AVG_42', 'AVG_43', 'AVG_44', 'AVG_45', 'AVG_46', 'AVG_47', 'AVG_48', 'AVG_49',
                     'AVG_50', 'AVG_51', 'AVG_52', 'AVG_53', 'AVG_54', 'AVG_55', 'AVG_56', 'AVG_57', 'AVG_58', 'AVG_59'
                     'AVG_60','AVG_61', 'AVG_62', 'AVG_63', 'AVG_64', 'AVG_65', 'AVG_66', 'AVG_67', 'AVG_68', 'AVG_69',
                     'AVG_70', 'AVG_71', 'AVG_72', 'AVG_73', 'AVG_74', 'AVG_75', 'AVG_76', 'AVG_77', 'AVG_78', 'AVG_79',
                     'AVG_80', 'AVG_81', 'AVG_82', 'AVG_83', 'AVG_84', 'AVG_85', 'AVG_86', 'AVG_87', 'AVG_88', 'AVG_89',
                     'AVG_90', 'AVG_91', 'AVG_92', 'AVG_93', 'AVG_94', 'AVG_95', 'AVG_96', 'AVG_97', 'AVG_98', 'AVG_99',
                   ]
        for field in range(0, len(VnameList)):
            f.write(VnameList[field])

        for row in range(len(data)):
            f.write(str(data[row]))
            f.write('   ')
        f.close()
        my_db.commit()

        return render(request, 'search4_1.html')

def search_data_4_2(request):
    date = [''] * 73
    attribute = [''] * 73
    if request.method=='POST':

        name = request.POST.get('name', None)
        attri = request.POST.get('attribute', None)
        start = request.POST.get('start', None)
        end = request.POST.get('end', None)


        start=start.replace('T',' ')
        end = end.replace('T', ' ')
        start=start+':00'
        end=end+':00'
        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        start = start.strftime('%m/%d/%Y %H:%M:%S')

        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        end = end.strftime('%m/%d/%Y %H:%M:%S')

        cursor = my_db.cursor(as_dict=True)
        cursor.execute('select *  from tbPRBnew where SECTOR_NAME= %s and (STARTTIME between %s and %s) ', (name, start, end))
        data = cursor.fetchall()
        for i in range(len(data)):
            date[i] = data[i]['STARTTIME']
            attribute[i] = data[i][attri]

        print(date)
        print(attribute)
        return render(request, 'search4_2.html', {"info1": date ,"info2": attribute})

    #统计小时级prb导出new

    #搜索new

#分析数据
def analyze_data_1(request):
    if request.POST:
        print('posting')
        SCELL = request.POST.get('SCELL', None)
        NCELL = request.POST.get('NCELL', None)
        cursor=my_db.cursor(as_dict=True)
        cursor.execute('select LteScRSRP,LteNcRSRP from tbMROData where ServingSector=%s and InterferingSector=%s',(SCELL,NCELL))
        result=cursor.fetchall()
        print(result)
        return render(request, 'analyz.html', {'info1': result})


def analyze_data_2(request):
    data={'C2I_Mean':'', 'Std':'', 'PrbC2I9': '','PrbABS6':''}
    if request.POST:
        print('posting')
        SCELL = request.POST.get('SCELL', None)
        NCELL = request.POST.get('NCELL', None)
        cursor2 = my_db.cursor()
        cursor2.execute('delete from tbC2Inew')
        my_db.commit()
        cursor=my_db.cursor()
        cursor.execute('exec C2I_Analyse 5')
        cursor1=my_db.cursor(as_dict=True)
        cursor1.execute('select C2I_Mean, Std from tbC2Inew where SCELL=%s and NCELL=%s',(SCELL,NCELL))
        result=cursor1.fetchall()

        mean=result[0]['C2I_Mean']

        std=result[0]['Std']
        PRB9=norm(mean,std,9)
        PRB6=norm(mean,std,6)
        PRB_6=norm(mean,std,-6)
        PRB6=PRB6-PRB_6
        data['C2I_Mean']=mean
        data['Std']=std
        data['PrbC2I9']=PRB9
        data['PrbABS6']=PRB6
        after=[data]
        print(data)
        return render(request, 'analyz.html', {'info':after})


#干扰
def search_interupt(request):
    if request.method=='POST':
        num = request.POST.get('value', None)
        cur = my_db.cursor()
        cur.execute('delete from tbC2I3')
        my_db.commit()
        cur2 = my_db.cursor()
        cur2.execute('delete from tbC2Inew')
        my_db.commit()
        cur3 = my_db.cursor()
        cur3.execute('exec C2I_Analyse 5')
        my_db.commit()
        select=my_db.cursor()
        select.execute('select C2I_Mean, Std, SCELL,NCELL from tbC2Inew')
        result = select.fetchall()
        for i in range(len(result)):
            SCELL=result[i][2]
            NCELL=result[i][3]
            if result[i][1]!=0:
                PRB9 = norm(result[i][0], result[i][1], 9)
                PRB6 = norm(result[i][0], result[i][1], 6)
            else:
                PRB9=0
                PRB6=0
            insert=my_db.cursor()
            insert.execute('update tbC2Inew set PrbC2I9=%d,PrbABS6=%d where SCELL=%s and NCELL=%s',(PRB9,PRB6,SCELL,NCELL))
            my_db.commit()

        cur4 = my_db.cursor()
        cur4.execute('exec generate_triSector %s',num)
        my_db.commit()
        cur5=my_db.cursor(as_dict=True)

        cur5.execute('select * from tbC2I3')

        data=cur5.fetchall()
        print(data)
        return render(request, 'interrupt.html', {'info': data})

