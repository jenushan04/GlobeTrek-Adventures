from django.contrib import admin
from .models import Inquiry, InquiryReply


class InquiryReplyInline(admin.TabularInline):
    model = InquiryReply
    extra = 0
    readonly_fields = ('staff', 'created_at')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'name', 'email', 'message')
    inlines = [InquiryReplyInline]


@admin.register(InquiryReply)
class InquiryReplyAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'staff', 'created_at')
    search_fields = ('reply', 'inquiry__subject')
