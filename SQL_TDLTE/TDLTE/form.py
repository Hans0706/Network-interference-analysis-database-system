#coding:utf-8
#将表单封装成class
from django import forms

#登陆表单
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"输入用户名","required":"required",}),
                               max_length=50,error_messages={"required":"用户名不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"输入密码","required":"required",}),
                               max_length=20,error_messages={"required":"密码不能为空",})
    # captcha = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"输入验证码","required":"required",}),
    #                            max_length=20,error_messages={"required":"验证码不能为空",})

#注册表单
class RegForm(forms.Form):                  #placeholder输入字段预期值的提示信息

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"用户名","required":"required",}),
                               max_length=50,error_messages={"required":"用户名不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"密码","required":"required",}),
                               max_length=20,error_messages={"required":"密码不能为空",})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"确认密码","required":"required",}),
                                       max_length=20,error_messages={"required":"密码不能为空",})

    def detect(self):   #自定义form的校验规则
        if not self.is_valid():  #required的字段有没有填写的is_valid()返回值就是false
            raise forms.ValidationError('所有项都必须填写')
        elif self.detected_data['confirm_password'] != self.detected_data['password']:
            raise forms.ValidationError('两次输入的密码不一致')
        else:
            detected_data = super(RegForm,self).detect()
        return detected_data   #clean()或clean_field()最后都必须返回验证完毕或者修改后的值


#文件表单
class ImportForm(forms.Form):
    file_name = forms.FileField(widget=forms.FileInput(attrs={"placeholder":"选择文件","required":"required",}),
                                max_length=100,error_messages={"required":"请选择数据源文件",})
    file_type = forms.CharField(widget=forms.Select(attrs={"placeholder":"选择文件格式","required":"required",}))
    table = forms.CharField(widget=forms.Select(attrs={"placeholder":"选择要导入的数据表","required":"required",}))
