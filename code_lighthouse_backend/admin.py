from django.contrib import admin

from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Comment

# Register your models here.

admin.site.register(Challenge)
admin.site.register(AppUser)
admin.site.register(Lighthouse)
admin.site.register(Assignment)
admin.site.register(Comment)
