from django.contrib import admin
from drop.models import Resume, ResumeBook, Company, DropEvent
from itertools import groupby
from django.core.files import File
import requests, os, errno, time
from pdf import PdfFileMerger
from models import get_book_path

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
        raise

class DropEventAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'ends', 'slug']
    readonly_fields = ['slug']
    search_fields = ['name']

class ResumeAdmin(admin.ModelAdmin):
    fields = ['name','industry','email','year','resume','event']
    search_fields = ['name','email']
    list_display = ['name','industry','email','year','event']

class ResumeBookAdmin(admin.ModelAdmin):
    fields = ['industry','year','book','events', 'resumes']
    readonly_fields = ['resumes']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['industry','year']
        return self.readonly_fields
    search_fields = ['industry','year']
    list_display = ['__unicode__','industry','year','events_string']
    def save_related(self, request, form, formsets, change):
        super(ResumeBookAdmin, self).save_related(request, form, formsets, change)
        instance = form.instance
        if not bool(instance.book):
            resumes_ungrouped = Resume.objects.filter(year=instance.year, industry=instance.industry, event__in=instance.events.all()).order_by('email', 'event')
            resumes = []
            for _, resume_group in groupby(resumes_ungrouped, key=lambda r: r.email):
                resume = list(resume_group)[-1]
                resume_loc = resume.path()
                mkdir_p('/'.join(resume_loc.split('/')[:-1]))
                try:
                    r = requests.get(resume.url())
                    with open(resume_loc, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)
                    resumes.append(resume)
                except:
                    continue
            merger = PdfFileMerger(strict=False)
            for pdf in resumes:
                try:
                    merger.append(pdf.path(), bookmark=pdf.name)
                except:
                    continue
            tmpfile = "/tmp/" + str(time.time()) + ".pdf"
            merger.write(tmpfile)
            merger.close()
            with open(tmpfile, 'r') as f:
                instance.book.save(get_book_path(instance,tmpfile), File(f))
            instance.resumes = resumes
            instance.save()

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name','contact_name','contact_email','industry','unique_hash']
    readonly_fields = ['unique_hash']
    search_fields = ['name']
    list_display = ['name','unique_hash', 'contact_name']

admin.site.register(DropEvent, DropEventAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeBook, ResumeBookAdmin)
admin.site.register(Company, CompanyAdmin)
