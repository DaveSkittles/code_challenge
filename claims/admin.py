from django.contrib import admin
from .models import Claim, Annotation


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_id', 'patient_name', 'billed_amount', 'paid_amount', 'status', 'flagged_for_review', 'created_at']
    list_filter = ['status', 'flagged_for_review', 'insurer_name']
    search_fields = ['claim_id', 'patient_name', 'insurer_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['claim', 'user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['claim__claim_id', 'content']
