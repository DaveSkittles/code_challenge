from django.db import models
from django.contrib.auth.models import User
import json


class Claim(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('underpaid', 'Underpaid'),
        ('pending', 'Pending'),
    ]
    
    claim_id = models.CharField(max_length=50, unique=True)
    patient_name = models.CharField(max_length=200)
    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Medical claim specific fields
    insurer_name = models.CharField(max_length=200)
    denial_reason = models.TextField(blank=True, null=True)
    cpt_codes = models.JSONField(default=list)  # List of CPT codes
    diagnosis_codes = models.JSONField(default=list)  # List of ICD codes
    service_date = models.DateField()
    provider_name = models.CharField(max_length=200)
    
    # Review fields
    flagged_for_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.claim_id} - {self.patient_name}"
    
    @property
    def underpaid_amount(self):
        return self.billed_amount - self.paid_amount
    
    class Meta:
        ordering = ['-created_at']


class Annotation(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='annotations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Annotation for {self.claim.claim_id} by {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
