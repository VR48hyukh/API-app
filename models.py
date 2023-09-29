from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class UserModel(models.Model):
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=100)
class Product(models.Model):
    title=models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(
        'UserModel',
        on_delete=models.CASCADE,
        related_name='products'
    )
    lessons = models.ManyToManyField(
        'LessonModel',
        through='LessonProductModel',
        related_name='products'
    )
    access = models.ManyToManyField(
        'UserModel',
        through='Access'
    )

class LessonModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    link = models.SlugField()
    views = models.ManyToManyField('UserModel',
		through='ViewsModel'
	)


class LessonProductModel(models.Model):
    lesson = models.ForeignKey('LessonModel', on_delete=models.CASCADE, related_name='plm')
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='plm')



class Access(models.Model):
	user = models.ForeignKey(
		'UserModel',
		on_delete=models.CASCADE,
		related_name='acc'
	)
	product = models.ForeignKey(
		'Product',
		on_delete=models.CASCADE,
		related_name='acc'
	)
	value = models.BooleanField(
		default=False
	)



class ViewsModel(models.Model):
    user = models.ForeignKey(
		'UserModel',
		on_delete=models.CASCADE,
		related_name='vws'
	)
    lesson = models.ForeignKey(
		'LessonModel',
		on_delete=models.CASCADE,
		related_name='vws'
	)
    duration = models.DurationField()
    date = models.DateTimeField(auto_now_add=True)