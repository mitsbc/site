from django.contrib import admin
from drop.models import Resume, ResumeBook, Company, DropEvent

class DropEventAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug']
    readonly_fields = ['slug']
    search_fields = ['name']

class ResumeAdmin(admin.ModelAdmin):
    fields = ['name','industry','email','year','resume']
    search_fields = ['name','email']
    list_display = ['name','industry','email','year']

class ResumeBookAdmin(admin.ModelAdmin):
    fields = ['industry','year','book']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('industry','year')
        return self.readonly_fields
    search_fields = ['industry','year']
    list_display = ['__unicode__','industry','year']

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name','contact_name','contact_email','industry','unique_hash']
    readonly_fields = ['unique_hash']
    search_fields = ['name']
    list_display = ['name','unique_hash', 'contact_name']

admin.site.register(DropEvent, DropEventAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeBook, ResumeBookAdmin)
admin.site.register(Company, CompanyAdmin)
