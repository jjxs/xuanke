from django.contrib import admin
from openpyxl import Workbook
# Register your models here.
from .models import Metting, UserMetting, User
from django.http import HttpResponse

admin.site.site_header = "超人罐头小程序后台"
class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(meta)
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for obj in queryset:
            for field in field_names:
                data = [str(getattr(obj, field)) for field in field_names]
            row = ws.append(data)

        wb.save(response)
        return response

    export_as_excel.short_description = '导出Excel'

@admin.register(UserMetting)
class UserMettingAdmin(admin.ModelAdmin, ExportExcelMixin):
    fields = ('user', 'metting', 'seat_num')
    list_display = ('user', 'metting', 'seat_num')
    search_fields = ('user', 'metting')
    list_filter = ('user', 'metting')
    actions = ['export_as_excel']

@admin.register(Metting)
class MettingAdmin(admin.ModelAdmin):
    fields = ('mettingName', 'config', 'time')
    list_display = ('mettingName', 'time','config')
    search_fields = ('mettingName', 'time')

@admin.register(User)
class MettingAdmin(admin.ModelAdmin):
    fields = ('openid', 'username', 'email')
    list_display = ('username','openid','email')
    search_fields = ('username', 'email')
