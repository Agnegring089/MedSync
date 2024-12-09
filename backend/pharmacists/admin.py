# farmaceuticos/admin.py

from django.contrib import admin
from .models import Pharmaceutical

class PharmaceuticalAdmin(admin.ModelAdmin):
    list_display = ('name', 'crf', 'user_email', 'status')
    list_editable = ('status',)
    list_filter = ('status',)
    search_fields = ('name', 'crf', 'user__email')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

admin.site.register(Pharmaceutical, PharmaceuticalAdmin)
