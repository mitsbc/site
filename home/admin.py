from django.contrib import admin
from home.models import Menu, MenuItem, SliderItem, Widget, CalendarItem, Member, MemberList

class MenuItemInline(admin.TabularInline):
    model = MenuItem.menus.through
    extra = 3

class MenuItemAdmin(admin.ModelAdmin):
    exclude = ['menus']
    list_display = ['text', 'page','link']
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

class MemberAdmin(admin.ModelAdmin):
    fields = ['name','title','email','department','year','image']
    list_display = ['name', 'email','year']
    search_fields = ['name']

class MemberListAdmin(admin.ModelAdmin):
    fields = ['name','title','member']
    search_fields = ['name','title']
    list_display = ['name','title']



admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(SliderItem, SliderItemAdmin)
admin.site.register(CalendarItem, CalendarItemAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberList, MemberListAdmin)