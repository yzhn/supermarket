from django import forms

from user.helper import set_password
from user.models import Register


class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={'required': '密码必填',
                                                'max_length': '字符不能超过16个',
                                                'min_length': '字符不能少于6'})
    password2 = forms.CharField(error_messages={'required': '密码不一致'})

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

    def clean_password(self):
        pd1 = self.cleaned_data.get('password1')
        pd2 = self.cleaned_data.get('password2')
        if pd1 and pd2 and pd1 != pd2:
            raise forms.ValidationError({'password2': '密码不正确'})
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
