from django.http import HttpResponse

from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option


from web import models



from django import forms
from django.db import transaction
from django.conf import settings






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

    action_list =[]

    # 批量申请客户到私户
    def multi_apply(self, request):
        pk_list = request.POST.getlist('pk')

        # 假设当前用户id为1
        current_user_id = 1

        # 计算当前销售手里 未报名的私户数量
        private_customer_count = models.Customer.objects.filter(consultant_id=current_user_id,status=2).count()

        # 判断该销售是否还能继续申请公户到自己手里
        if (private_customer_count + len(pk_list)) > settings.MAX_PRIVATE_CUSTOMER_COUNT:
            return HttpResponse('要这么多干鸡毛')

        # 解决“并发抢单”问题，销售 A 和销售 B 同时盯着公海里的“马云”，同时勾选并点击申请，到底算谁的？
        # 加排他锁
        try:
            flag = False
            with transaction.atomic():
                # 排他锁: .select_for_update()
                origin_queryset = models.Customer.objects.filter(id__in=pk_list,status=2,consultant_id__isnull=True,).select_for_update()

                if len(pk_list) == len(origin_queryset):
                    origin_queryset.update(consultant_id=current_user_id)
                    flag = True

            if not flag:
                return HttpResponse('手速还得练')

        except Exception as e:
            print(str(e))


    multi_apply.text = '批量申请'
    action_list.append(multi_apply)


    list_display = [
        StarkConfig.display_checkbox,
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

    action_list = []

    # 将客户从私户移除至公户
    def multi_remove(self, request):
        pk_list = request.POST.getlist('pk')
        # 假设当前用户id为1
        current_user_id = 1
        self.model_class.objects.filter(id__in=pk_list,consultant_id=current_user_id,).update(consultant=None)

    multi_remove.text = '移除客户'
    action_list.append(multi_remove)



    model_form_class = PrivateModelForm

    list_display = [
        StarkConfig.display_checkbox,
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
