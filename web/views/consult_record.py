from django.http import HttpResponse

from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option


from web import models



from django import forms
from django.db import transaction
from django.conf import settings



class ConsultRecordConfig(StarkConfig):

    def get_queryset(self):
        cid = self.request.GET.get('cid')
        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid)
        return self.model_class.objects


    list_display = ['customer','note','consultant','date']



class PriModelFrom(BootStrap,forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['customer','consultant',]


class PriConsultRecordConfig(StarkConfig):



    model_form_class = PriModelFrom

    def save(self, form, is_modify=True, *args, **kwargs):
        if not is_modify:
            # 假设当前用户id为1
            current_user_id = 1
            # 获取原条件
            params = self.request.GET.get('_filter')
            cid, num = params.split('=',maxsplit=1)

            form.instance.customer = models.Customer.objects.filter(pk=num).first()
            form.instance.consultant = models.UserInfo.objects.filter(pk=current_user_id).first()
            form.save()

    def get_queryset(self):
        # 假设当前用户id为1
        current_user_id = 1
        cid = self.request.GET.get('cid')

        if cid:
            return models.ConsultRecord.objects.filter(customer_id=cid,customer__consultant_id=current_user_id)
        return self.model_class.objects.filter(consultant_id=current_user_id)


    list_display = ['customer','note','consultant','date']






