from stark.service.stark import StarkConfig,get_choice_text



from django.http import HttpResponse
from django.urls import path,reverse
from django.utils.safestring import mark_safe






class UserInfoConfig(StarkConfig):

    def extra_url(self):
        prefix = f'{self.model_class._meta.app_label}_{self.model_class._meta.model_name}'

        urlpatterns = [
            path('detail/<int:pk>/', self.wrapper(self.detail_view), name=f'{prefix}_detail'),
        ]

        return urlpatterns

    def detail_view(self,request,pk):
        return HttpResponse('用户详细')


    def display_detail(self, obj=None, header=False):
        if header:
            return '查看详细'

        url = reverse('stark:web_userinfo_detail',kwargs={'pk':obj.id})
        return mark_safe(f'<a href="{url}">{obj.name}</a>')


    list_display = [
        display_detail,
        get_choice_text('gender','性别'),
        'phone',
        'email',
        'depart',
        StarkConfig.display_edit_del,
    ]