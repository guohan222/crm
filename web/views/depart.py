from stark.service.stark import StarkConfig

class DepartmentConfig(StarkConfig):
    list_display = ['title',StarkConfig.display_edit_del,]