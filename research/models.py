from django.db import models


class Research(models.Model):
    LENGTH_CHOICES = [
        ("short", "Short"),
        ("medium", "Medium"),
        ("long", "Long"),
    ]

    TONE_CHOICES = [
        ("professional", "Professional"),
        ("casual", "Casual"),
        ("academic", "Academic"),
        ("friendly", "Friendly"),
    ]

    STATUS_CHOICES = [
          ("pending", "Pending"),
          ("in_progress", "In Progress"),
          ("completed", "Completed"),
          ("failed", "Failed"),
    ] 

    STAGE_CHOICES = [
        ("research", "Research Agent"),
        ("planning", "Planning Agent"),
        ("writing", "Writing Agent"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    topic = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, default="")
    article_length = models.CharField(
        max_length=20,
        choices=LENGTH_CHOICES,
        default="medium",
    )
    tone = models.CharField(
        max_length=20,
        choices=TONE_CHOICES,
        default="professional",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
    )
    current_stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default="research",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.topic


class Article(models.Model):
    research = models.OneToOneField(
        Research,
        on_delete=models.CASCADE,
        related_name="article",
    )
    title = models.CharField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title