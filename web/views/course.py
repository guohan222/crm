from stark.service.stark import StarkConfig

class CourseConfig(StarkConfig):
    list_display = ['name',StarkConfig.display_edit_del,]