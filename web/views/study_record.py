from django import forms
from django.urls import path
from django.db import transaction
from django.conf import settings
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option


from web import models









class StudyRecordModelForm(BootStrap,forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['record']


class StudyRecordConfig(StarkConfig):


    # 为每张表生成crud路由
    def get_urls(self):
        urlpatterns = [
            path('list/', self.wrapper(self.changelist_view), name=self.get_list_url_name),
        ]

        return urlpatterns



    def changelist_view(self, request, *args, **kwargs):
        # 课程记录
        crid = request.GET.get('crid')

        model_formset_cls = modelformset_factory(models.StudyRecord,StudyRecordModelForm,extra=0)
        queryset = models.StudyRecord.objects.filter(course_record_id=crid)

        if request.method == 'GET':
            formset = model_formset_cls(queryset=queryset)
            return render(request,'study_record.html',{'formset':formset})

        formset = model_formset_cls(queryset=queryset,data=request.POST)
        print(formset.errors)
        if formset.is_valid():
            formset.save()
            return render(request, 'study_record.html', {'formset': formset})

        return render(request, 'study_record.html', {'formset': formset})



