from django.shortcuts import render
from django.core.files.storage import default_storage, FileSystemStorage
from .forms import ImageUploadForm
from .face_swap_utils import read_image, swap_faces
from PIL import Image
import cv2
import io


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source_image = form.cleaned_data['source_image']
            target_image = form.cleaned_data['target_image']

            # Сохранение загруженных файлов изображений
            source_image_path = default_storage.save(source_image.name, source_image)
            target_image_path = default_storage.save(target_image.name, target_image)

            # Чтение изображений
            with default_storage.open(source_image_path, 'rb') as source_file:
                src_img = read_image(source_file)
            with default_storage.open(target_image_path, 'rb') as target_file:
                tgt_img = read_image(target_file)

            swapped_image, error = swap_faces(src_img, tgt_img)
            if error:
                return render(request, 'face_swap/index.html', {'form': form, 'error': error})

            # Конвертирование изображения в байты и сохранение
            swapped_image_pil = Image.fromarray(cv2.cvtColor(swapped_image, cv2.COLOR_BGR2RGB))
            byte_io = io.BytesIO()
            swapped_image_pil.save(byte_io, format='JPEG')
            byte_io.seek(0)

            fs = FileSystemStorage()
            swapped_image_path = fs.save('swapped_image.jpg', byte_io)

            return render(request, 'face_swap/result.html', {
                'source_image_url': default_storage.url(source_image_path),
                'target_image_url': default_storage.url(target_image_path),
                'swapped_image_url': fs.url(swapped_image_path)
            })
    else:
        form = ImageUploadForm()
    return render(request, 'face_swap/index.html', {'form': form})
