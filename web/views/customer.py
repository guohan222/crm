from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option


from web import models


from django import forms


class CustomerConfig(StarkConfig):
    list_display = [
        'name',
        'qq',
        get_choice_text('status', '状态'),
        get_choice_text('gender', '性别'),
        get_choice_text('source', '来源'),
    ]

    order_by = ['-id']

    search_list = ['name', 'qq']

    search_group = [
        Option('status', is_choice=True),
        Option('gender', is_choice=True),
        Option('source', is_choice=True),
    ]





















# 公户

class PublicCustomerConfig(StarkConfig):

    def get_queryset(self):
        return self.model_class.objects.filter(consultant__isnull=True)

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_del)
        return val

    list_display = [
        'name',
        'qq',
        get_choice_text('status', '状态'),
        get_choice_text('gender', '性别'),
        get_choice_text('source', '来源'),
    ]

    order_by = ['-id']

    search_list = ['name', 'qq']

    search_group = [
        Option('status', is_choice=True),
        Option('gender', is_choice=True),
        Option('source', is_choice=True),
    ]


























# 私户

class PrivateModelForm(BootStrap,forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant',]


class PrivateCustomerConfig(StarkConfig):

    def save(self,form,is_modify=True,*args,**kwargs):
        # 假设当前用户id为1
        current_user_id = 1

        form.instance.consultant = models.UserInfo.objects.filter(pk=current_user_id).first()

        form .save()

    def get_queryset(self):
        # 显示当前用户自己的私户
        # 假设当前用户id为1
        current_user_id = 1
        return self.model_class.objects.filter(consultant_id=current_user_id)


    def get_list_display(self):
        """获取要显示的字段（列），预留的自定义扩展，例如：以后根据用户的不同显示不同的列"""
        val = super().get_list_display()
        val.remove(StarkConfig.display_del)
        return val

    model_form_class = PrivateModelForm

    list_display = [
        'name',
        'qq',
        get_choice_text('status','状态'),
        get_choice_text('gender','性别'),
        get_choice_text('source','来源'),
    ]

    order_by = ['-id']

    search_list = ['name','qq']

    search_group = [
        Option('status',is_choice=True),
        Option('gender',is_choice=True),
        Option('source',is_choice=True),
    ]
