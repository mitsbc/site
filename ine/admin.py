from django.contrib import admin
from ine.models import Resume, ResumeBook, Company

class ResumeAdmin(admin.ModelAdmin):
    fields = ['name','email','year','resume']
    search_fields = ['name','email']
    list_display = ['name','email','year']

class ResumeBookAdmin(admin.ModelAdmin):
    fields = ['_type','year','book']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('_type','year')
        return self.readonly_fields
    search_fields = ['_type','year']
    list_display = ['__unicode__','_type','year']

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name','contact_name','contact_email','_type','_hash']
    readonly_fields = ['_hash']
    search_fields = ['name']
    list_display = ['name','_hash', 'contact_name']

admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeBook, ResumeBookAdmin)
admin.site.register(Company, CompanyAdmin)