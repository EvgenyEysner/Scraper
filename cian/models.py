from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image as Img

User = get_user_model()


class Apartment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rooms = models.CharField("кол-во комнат", max_length=64, blank=True)
    price = models.CharField("цена", max_length=20, blank=True)
    address = models.CharField("Адрес", max_length=256, blank=True)
    desc = models.TextField("описание", blank=True)
    floor = models.CharField("этаж", max_length=10, blank=True)
    commission = models.CharField("коммисия", max_length=256, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "квартира"
        verbose_name_plural = "квартиры"


class Image(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    img = models.ImageField(upload_to="image/", blank=True)

    def save(self, *args, **kwargs):
        super().save()
        image = Img.open(self.img.path)
        cropped_image = image.crop((0, 0, 700, 650))  # лево, верх, право, низ
        cropped_image.save(self.img.path)

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    url = models.URLField("ссылка")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "ссылка"
        verbose_name_plural = "ссылки"
        ordering = ["-created"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField("имя", max_length=120, blank=True)
    last_name = models.CharField("фамилия", max_length=240, blank=True)
    phone_1 = models.CharField("телефон 1", max_length=18, blank=True)
    phone_2 = models.CharField("телефон 2", max_length=18, blank=True)
    avatar = models.ImageField(
        "аватар", default="avatars/avatar.png", upload_to="avatars/%Y/%m/%d"
    )
    email = models.EmailField("email")

    def __str__(self):
        return "Профиль пользователя %s" % self.user

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
