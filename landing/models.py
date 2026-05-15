from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.question[:50]}"


class DurianQuery(models.Model):
    VARIETY_CHOICES = [
        ('musang_king', 'Musang King'),
        ('monthong', 'Monthong'),
        ('d24', 'D24'),
        ('xo', 'XO'),
        ('black_thorn', 'Black Thorn'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query_text = models.TextField()
    variety = models.CharField(max_length=50, choices=VARIETY_CHOICES, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.query_text[:50]}"


class LeafIdentification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaf_ids')
    image = models.ImageField(upload_to='leaves/')
    identified_variety = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)
    leaf_features = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.identified_variety or 'Unknown'}"