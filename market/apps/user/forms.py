from datetime import date

from django import forms
from django_redis import get_redis_connection

from user.helper import set_password
from user.models import Register, UserAddress


class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={'required': '密码必填',
                                                'max_length': '字符不能超过16个',
                                                'min_length': '字符不能少于6'})
    password2 = forms.CharField(error_messages={'required': '密码不一致'})

    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写"
                              })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议'
    })

    class Meta:
        model = Register
        fields = ['phone', ]
        error_messages = {'phone': {'required': '手机号码必填'}}

    # 验证手机号码是否被注册
    def clean_phone(self):
        # 获取清洗后的手机号码
        phone = self.cleaned_data.get('phone')
        # 在数据库中匹配
        rs = Register.objects.filter(phone=phone).exists()
        # 存在就抛出异常
        if rs:
            raise forms.ValidationError('号码已备注册')
        return phone

    # 综合校验
    def clean_password(self):
        pd1 = self.cleaned_data.get('password1')
        pd2 = self.cleaned_data.get('password2')
        # 比较两次输入的密码是否一致,不一致时抛出错误
        if pd1 and pd2 and pd1 != pd2:
            raise forms.ValidationError({'password2': '密码不正确'})

            # 验证 用户传入的验证码和redis中的是否一样
            # 用户传入的
        try:
            captcha = self.cleaned_data.get('captcha')
            phone = self.cleaned_data.get('phone', '')
            # 获取redis中的
            red = get_redis_connection()
            random_code = red.get(phone)
            # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})
        return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['phone', 'password']

        error_messages = {
            'phone': {'required': '请填写手机号', },
            'password': {'required': '请填写密码', }
        }

    def clean(self):
        # 获取用户名和密码
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')

        # 验证
        # 根据手机号码获取
        try:
            user = Register.objects.get(phone=phone)
        except Register.DoesNotExist:
            raise forms.ValidationError({'phone': '手机号错误'})

        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写错误'})

        # 将用户信息保存到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


class ForgetPasswordModelForm(forms.ModelForm):
    pwd1 = forms.CharField(max_length=16, min_length=6, error_messages={'required': '密码必填',
                                                                        'max_length': '字符个数不能超过16位',
                                                                        'min_length': '字符个数不能少于6位'})
    pwd2 = forms.CharField(error_messages={"required": '密码不一致'})

    class Meta:
        model = Register
        fields = ['phone', ]
        error_messages = {'phone': {'required': '手机号码必填'}}

    def clean_phone(self):
        # 获取清洗后的数据
        phone = self.cleaned_data.get('phone')
        # 在数据库中匹配
        rs = Register.objects.filter(phone=phone).exists()
        # 不存在就抛出异常
        if rs is None:
            raise forms.ValidationError('号码不正确')
        return phone

    def clean(self):
        #  获取两次输入的手机号码
        pd1 = self.cleaned_data.get('pwd1')
        pd2 = self.cleaned_data.get('pwd2')
        # 比较两次的手机号码是否一致
        if pd1 and pd2 and pd1 != pd2:
            raise forms.ValidationError({'password2': '密码不正确'})
        return self.cleaned_data


class ReviseModelForm(forms.ModelForm):
    pwd1 = forms.CharField(max_length=16, min_length=6, error_messages={'required': '密码必填',
                                                                        'max_length': '字符个数不能超过16位',
                                                                        'min_length': '字符个数不能少于6位'})
    pwd2 = forms.CharField(error_messages={"required": '密码不一致'})

    class Meta:
        model = Register
        fields = ['password', ]
        error_messages = {'password': {'required': '密码必填'}}

    def clean_phone(self):
        # 获取清洗后的数据
        password = self.cleaned_data.get('password')
        # 在数据库中匹配
        rs = Register.objects.filter(password=password).exists()
        # 存在就抛出异常
        if rs.DosNotExist:
            raise forms.ValidationError('密码不正确')
        return password

    def clean(self):
        #  获取两次输入的手机号码
        pd1 = self.cleaned_data.get('pwd1')
        pd2 = self.cleaned_data.get('pwd2')
        # 比较两次的手机号码是否一致
        if pd1 and pd2 and pd1 != pd2:
            raise forms.ValidationError({'password2': '密码不正确'})
        return self.cleaned_data


class MemberModelForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['birthday', ]
        error_messages = {'birthday': {'required': '日期格式不对'}}

    def cleaned_data(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday > date.today():
            raise forms.ValidationError('出生日期应小于今天')
        return birthday


class AddressAddForm(forms.ModelForm):
    """用户添加收货地址的表单"""

    class Meta:
        model = UserAddress
        exclude = ['create_time', 'update_time', 'is_delete', 'user']
        error_messages = {
            'username': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'brief': {
                'required': "请填写详细地址！",
            },
            'hcity': {
                'required': "请填写完整地址！",
            },
            'hproper': {
                'required': "请填写完整地址！",
            },
            'harea': {
                'required': "请填写完整地址！",
            },
        }

    def clean(self):
        # 验证如果数据库里地址已经超过6六表报错
        cleaned_data = self.cleaned_data
        count = UserAddress.objects.filter(user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"hcity": "收货地址最多只能保存6条"})
        return cleaned_data
