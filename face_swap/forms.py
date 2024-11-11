from django import forms

# Создание форм для загрузки изображений
class ImageUploadForm(forms.Form):
    source_image = forms.ImageField(label='Source Image')
    target_image = forms.ImageField(label='Target Image')
