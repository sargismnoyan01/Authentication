from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from app_core.models import SingltoneClass

class MyUser(AbstractUser):
    phone = PhoneNumberField('Phone',help_text='for example +37455555555')
    qr_code = models.ImageField(upload_to='qr_code',blank=True)
    verify_code = models.IntegerField('verify code',blank=True)
    is_verify = models.BooleanField('is_verify',default=False)
    img = models.ImageField('User Image',upload_to='user_images',null=True,default='m7XuV1i6egth4ISiD240.jpg')
    position = models.CharField('Position',max_length=255,null=True)
    gender = models.CharField(choices=[('Male',"Male"),("Female",'Female')],null=True,max_length=255)
    age = models.IntegerField('Age',null=True)

    

class UserConfig(SingltoneClass):
    max_login_attempts = models.IntegerField(default=5)
    session_timeout = models.IntegerField(default=15)


class Product(models.Model):
    name=models.CharField('Product name',max_length=255)
    img = models.ImageField('image',upload_to='products')
    price = models.IntegerField('Price')


    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Product'
        verbose_name_plural='Products'
































































































