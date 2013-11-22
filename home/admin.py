from django.contrib import admin
from home.models import Menu, MenuItem, SliderItem, Widget, CalendarItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem.menus.through
    extra = 3

class MenuItemAdmin(admin.ModelAdmin):
    exclude = ['menus']
    list_display = ('text', 'link','page')
    search_fields = ['text']

class MenuAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = [MenuItemInline]
    search_fields = ['name']

class SliderItemAdmin(admin.ModelAdmin):
    fields = ['text','link','image','new_page']
    search_fields = ['text']

class CalendarItemAdmin(admin.ModelAdmin):
    fields = ['name','location','time','link','new_page']
    search_fields = ['name']

class WidgetAdmin(admin.ModelAdmin):
    fields = ['name','title','contents']
    search_fields = ['title']




admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(SliderItem, SliderItemAdmin)
admin.site.register(CalendarItem, CalendarItemAdmin)
admin.site.register(Widget, WidgetAdmin)