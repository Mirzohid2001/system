from django.db import models
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey


PLAN_CHOICES = (
    ('top', 'Top'),       
    ('medium', 'Medium'), 
    ('basic', 'Basic'),   
)

PLAN_PRIORITY = {
    'top': 3,
    'medium': 2,
    'basic': 1
}

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived')
)

class AnalyticsDummy(models.Model):
    class Meta:
        verbose_name = "Аналитика"
        verbose_name_plural = "Аналитика"

    def __str__(self):
        return "Analytics Data"

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog/category/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.CharField(max_length=50, blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    priority = models.IntegerField(default=1) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.priority = PLAN_PRIORITY.get(self.plan, 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='announcements/')

    def __str__(self):
        return f"Image of {self.announcement.title}"

    class Meta:
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'

class Payment(models.Model):
    PLAN_AMOUNTS = {
        'top': 100000,
        'medium': 50000,
        'basic': 10000
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.PLAN_AMOUNTS.get(self.plan, 10000)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} -> {self.plan} ({self.amount})"
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    
class Favorite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')

    def __str__(self):
        return f"{self.user.username} favorite -> {self.announcement.title}"
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    class Meta:
        unique_together = ('user', 'announcement')
    
class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.announcement.title}"
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


