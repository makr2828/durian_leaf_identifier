from django.contrib import admin
from .models import ChatHistory, DurianQuery, LeafIdentification


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_preview', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['question', 'answer']

    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question

    question_preview.short_description = 'Question'


@admin.register(DurianQuery)
class DurianQueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query_preview', 'variety', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'variety']
    list_editable = ['is_resolved']

    def query_preview(self, obj):
        return obj.query_text[:50] + '...' if len(obj.query_text) > 50 else obj.query_text


@admin.register(LeafIdentification)
class LeafIdentificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'identified_variety', 'confidence_score', 'created_at']
    list_filter = ['identified_variety', 'created_at']
    readonly_fields = ['image']