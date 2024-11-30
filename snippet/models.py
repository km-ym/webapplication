from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField('タグ', max_length=50)

    def __str__(self):
        return self.name

class Code(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=200)
    code = models.TextField(verbose_name='コード')
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT, blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="タグ", blank=True)
    relation = models.ManyToManyField('self', verbose_name='関連', blank=True)
    description = models.TextField(verbose_name='メモ', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日', null=False, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新日',null=False, auto_now=True)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('list')
    
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_codes = models.ManyToManyField(Code, blank=True, related_name='favorite_by')

    def __str__(self):
        return self.user.username
    
class UserProfileManager:
    @staticmethod
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    @staticmethod
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

# シグナルでUserProfile作成・保存処理を呼び出し
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=UserProfile)
def save_user_profile(sender, instance, **kwargs):
    UserProfileManager.save_user_profile(sender, instance, **kwargs)