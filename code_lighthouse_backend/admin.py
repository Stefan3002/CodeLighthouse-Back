from django.contrib import admin

from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Comment, Like, Code, Submission, \
    Reports, Announcement, Notification

# Register your models here.

admin.site.register(Challenge)
admin.site.register(AppUser)
admin.site.register(Lighthouse)
admin.site.register(Assignment)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Code)
admin.site.register(Submission)
admin.site.register(Reports)
admin.site.register(Announcement)
admin.site.register(Notification)
