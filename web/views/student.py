from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option

from web import models
from web.utils.mixins import PermissionMixins

from django.http import HttpResponse
from django import forms
from django.db import transaction
from django.conf import settings




class StudentConfig(PermissionMixins,StarkConfig):

    def display_class_list(self, obj=None, header=False):
        if header:
            return '班级'
        # 打印一个 集合类型（List、Dict、Tuple）时，为了防止产生歧义，Python 规定：列表内部的元素，不再调用 __str__，而是强制调用 __repr__
        # Django 底层源码里写死了，Model 的 __repr__ 格式必须是：<模型名: 对象的__str__结果>，而< >会使浏览器误解
        # 处理多对多字段（M2M）拿到的 QuerySet 或者列表时，必须手动用一个 for 循环把对象一个个掏出来，强行对它进行 str(item) 或者提取它的特定属性，然后再自己拼成字符串返回
        return '、'.join([str(item) for item in obj.class_list.all()])


    list_display = ['customer',display_class_list]