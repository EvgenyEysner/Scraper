from django.forms import ModelForm, URLInput, HiddenInput, FloatField, FileInput, Form, TextInput
from .models import Apartment, Image, Profile
from PIL import Image as Img


class ButtonForm(Form):
        button = TextInput
        widgets = {
            'url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'ссылка...',
            }),
        }


class ApartmentEditForm(ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'


class ImageForm(ModelForm):
    x = FloatField(widget=HiddenInput())
    y = FloatField(widget=HiddenInput())
    width = FloatField(widget=HiddenInput())
    height = FloatField(widget=HiddenInput())

    class Meta:
        model = Image
        fields = ('img', 'x', 'y', 'width', 'height', )

        widgets = {
            FileInput(attrs={
                'class': 'form-control',
            }),
        }

    # needed to crop a photo, override the method save
    def save(self):
        photo = super(ImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Img.open(photo.img) # Pillow
        cropped_image = image.crop((x, y, w+x, h+y)) # crop the image
        resized_image = cropped_image.resize((400, 400), Img.ANTIALIAS) # resize cropped image
        resized_image.save(photo.img.path) # save resized image

        return resized_image


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'first_name', 'last_name', 'email', 'phone_1', 'phone_2')