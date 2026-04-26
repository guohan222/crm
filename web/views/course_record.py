from django.http import HttpResponse
from django.utils.safestring import mark_safe

from stark.form.bootstrap import BootStrap
from stark.service.stark import StarkConfig, get_choice_text, Option


from web import models



from django import forms
from django.db import transaction
from django.conf import settings



class CourseRecordConfig(StarkConfig):

    def display_title(self, obj=None, header=False):
        if header:
            return '上课记录'
        tpl = f'{obj.class_object}-day{obj.day_num}'
        return tpl

    action_list = []
    def multi_init(self, request):
        """批量初始化"""
        # 选中的上课记录
        pk_list = request.POST.getlist('pk')

        # 循环每个上课记录，为每课里面的所有学生进行学习记录的初始化
        for pk in pk_list:
            # 找到这个上课记录记录对象
            record_obj = models.CourseRecord.objects.filter(pk=pk).first()
            # 找到这个课的所有学生
            stu_list = models.Student.objects.filter(class_list=record_obj.class_object)

            # 如果这个上课记录在学生考勤记录中已经存在了则不在进行初始化 (即这天的上课已经对学生上课考勤初始化了)
            exists = models.StudyRecord.objects.filter(course_record=record_obj).exists()
            if exists:
                continue

            # 统一初始化
            study_record_list = []
            for item in stu_list:
                study_record_list.append(models.StudyRecord(student=item,course_record=record_obj))

            models.StudyRecord.objects.bulk_create(study_record_list)

    # 一切皆对象
    multi_init.text = '批量初始化'
    action_list.append(multi_init)




    list_display = [StarkConfig.display_checkbox,display_title,]
