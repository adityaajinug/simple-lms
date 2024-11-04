from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField("Nama Kursus", max_length=100)
    description = models.TextField("Deskripsi")
    price = models.IntegerField("Harga")
    image = models.ImageField("Gambar", upload_to="courses", null=True)
    teacher = models.ForeignKey(User, verbose_name="Penajar", on_delete=models.RESTRICT)
    created_at = models.DateTimeField("Dibuat pada",auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada",auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kursus"
        verbose_name_plural = "Data Kursus"
        ordering = ['-created_at']