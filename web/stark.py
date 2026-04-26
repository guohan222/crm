from stark.service.stark import site


from web import models
from web.views.school import SchoolConfig
from web.views.depart import DepartmentConfig
from web.views.userinfo import UserInfoConfig
from web.views.class_list import ClassListConfig
from web.views.course import CourseConfig
from web.views.customer import CustomerConfig,PublicCustomerConfig,PrivateCustomerConfig
from web.views.consult_record import ConsultRecordConfig,PriConsultRecordConfig
from web.views.student import StudentConfig
from web.views.course_record import CourseRecordConfig







site.register(models.School,SchoolConfig)
site.register(models.Department,DepartmentConfig)
site.register(models.UserInfo,UserInfoConfig)
site.register(models.ClassList,ClassListConfig)
site.register(models.Course,CourseConfig)
site.register(models.Customer,CustomerConfig)
site.register(models.Customer,PublicCustomerConfig,'pub')
site.register(models.Customer,PrivateCustomerConfig,'pri')
site.register(models.ConsultRecord,ConsultRecordConfig)
site.register(models.ConsultRecord,PriConsultRecordConfig,'pri')
site.register(models.Student,StudentConfig)
site.register(models.CourseRecord,CourseRecordConfig)