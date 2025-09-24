from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['order', 'to_user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['order__id', 'to_user__username']
    ordering = ['-created_at']
