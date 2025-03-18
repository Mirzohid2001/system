from django.db import models
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey

PLAN_CHOICES = [
    ('basic', 'Basic'),
    ('standard', 'Standard'),
    ('top', 'Top'),
]

class Plan(models.Model):
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.get_name_display()} - {self.amount} RUB"

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'

PLAN_PRIORITY = {
    'top': 3,
    'medium': 2,
    'basic': 1
}

def save(self, *args, **kwargs):
    self.priority = PLAN_PRIORITY.get(self.plan, 1)
    super().save(*args, **kwargs)

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
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.IntegerField(default=1) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.priority = PLAN_PRIORITY.get(self.plan, 1)
        super().save(*args, **kwargs)

    def get_position_label(self):
        if self.plan == 'top':
            return "Top of the board"
        elif self.plan == 'medium':
            return "Middle of the board"
        else:
            return "Lower part of the board"
            
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.amount})"
    
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

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новость'    
        verbose_name_plural = 'Новости'

class Chat(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.announcement:
            return f"Chat about Announcement: {self.announcement.title}"
        return "General Chat"
    
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    



    


        




