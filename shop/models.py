from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)
	image = models.ImageField(upload_to='products/%Y/%m/%d')
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'), )

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail', args=[self.id, self.slug])

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	portfolio_site = models.URLField(blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

	def __str__(self):
		return self.user.username