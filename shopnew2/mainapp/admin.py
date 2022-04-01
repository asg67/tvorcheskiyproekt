from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField, ModelForm, ValidationError
# Register your models here.
from  .models import *
from PIL import Image
from django.utils.safestring import mark_safe


class CoffeeAdminForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с минимальным разрешением {}x{}</span>'.format(
            *Product.MIN_RESOLUTION
        ))

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МВ!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешения изображение меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешения изображение больше максимального!')
        return image



class CoffeeAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='coffee'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)