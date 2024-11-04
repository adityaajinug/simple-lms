from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField("Nama Kursus", max_length=100)
    description = models.TextField("Deskripsi")
    price = models.IntegerField("Harga")
    image = models.ImageField("Gambar", upload_to="courses", null=True)
    teacher = models.ForeignKey(User, verbose_name="Pengajar", on_delete=models.RESTRICT)
    created_at = models.DateTimeField("Dibuat pada", auto_now_add=True)
    updated_at = models.DateTimeField("Diperbarui pada", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kursus"
        verbose_name_plural = "Data Kursus"
        ordering = ['-created_at']

ROLE_OPTIONS = [('std', "Siswa"), ('ast', "Asisten")]

class CourseMember(models.Model):
    course = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    user = models.ForeignKey(User, verbose_name="siswa", on_delete=models.RESTRICT)
    roles = models.CharField("peran", max_length=3, choices=ROLE_OPTIONS, default='std')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscriber Matkul"
        verbose_name_plural = "Subscriber Matkul"

    def __str__(self):
        return f"{self.course.name} : {self.user.username}"

class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')
    video_url = models.CharField("URL Video", max_length=200, null=True, blank=True)
    file_attachment = models.FileField("File", upload_to="course_content_files", null=True, blank=True)
    course = models.ForeignKey(Course, verbose_name="matkul", on_delete=models.RESTRICT)
    parent = models.ForeignKey("self", verbose_name="induk", on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konten Matkul"
        verbose_name_plural = "Konten Matkul"

    def __str__(self):
        return f"[{self.course.name}] {self.name}"

class Comment(models.Model):
    content = models.ForeignKey(CourseContent, verbose_name="konten", on_delete=models.CASCADE)
    member = models.ForeignKey(CourseMember, verbose_name="pengguna", on_delete=models.CASCADE)
    comment = models.TextField("komentar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Komentar"
        verbose_name_plural = "Komentar"

    def __str__(self):
        return f"Komen: {self.content.name} - {self.member.user.username}"
