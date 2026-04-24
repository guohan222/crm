from stark.service.stark import StarkConfig, get_choice_text, Option


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



class PublicCustomerConfig(StarkConfig):

    def get_queryset(self):
        return self.model_class.objects.filter(consultant__isnull=True)


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



class PrivateCustomerConfig(StarkConfig):


    def get_queryset(self):
        # 显示当前用户自己的私户
        # 假设当前用户id为1
        current_user_id = 1
        return self.model_class.objects.filter(consultant_id=current_user_id)


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
