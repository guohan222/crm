from stark.service.stark import StarkConfig, Option

class ClassListConfig(StarkConfig):

    def display_title(self, obj=None, header=False):
        if header:
            return '班级'

        return f'{obj.course.name}-{obj.semester}期'

    list_display = ['id',display_title,'school','start_date',]
    search_group = [
        Option(field='school',is_choice=False,is_multi=False,text_func=lambda x:x.title,value_func=lambda x:x.pk),
        Option(field='course',is_choice=False,is_multi=False,text_func=lambda x:x.name,value_func=lambda x:x.pk)
    ]