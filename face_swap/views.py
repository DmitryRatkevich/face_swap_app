from django.shortcuts import render
from .forms import ImageUploadForm
from django.core.files.storage import default_storage

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source_image = form.cleaned_data['source_image']
            target_image = form.cleaned_data['target_image']
            # Сохранение загруженных изображений
            source_image_name = default_storage.save(source_image.name, source_image)
            target_image_name = default_storage.save(target_image.name, target_image)
            return render(request, 'face_swap/result.html', {
                'source_image_url': default_storage.url(source_image_name),
                'target_image_url': default_storage.url(target_image_name)
            })
    else:
        form = ImageUploadForm()
    return render(request, 'face_swap/index.html', {'form': form})
