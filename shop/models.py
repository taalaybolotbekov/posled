from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    


class Product(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    oldprice = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField() #delete
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name_plural = "shop"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class Applications(models.Model):
    name = models.CharField(verbose_name = 'Имя', max_length=30)
    mail = models.CharField(verbose_name = 'Почта',max_length=100)
    subject = models.CharField(verbose_name = 'Тема',max_length=200)
    comment = models.TextField(verbose_name = 'Коммент')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Заявка cо страницы контактов'
        verbose_name_plural = 'Заявка со страницы контактов'