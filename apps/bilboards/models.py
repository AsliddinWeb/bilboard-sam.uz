from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Manzil nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"

class Region(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='regions', verbose_name="Manzil")
    name = models.CharField(max_length=100, verbose_name="Viloyat nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name="Viloyat")
    name = models.CharField(max_length=100, verbose_name="Tuman nomi")

    def __str__(self):
        return f"{self.region.name} - {self.name}"

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"


class Billboard(models.Model):
    STATUS_CHOICES = (
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
    )

    image = models.ImageField(upload_to='billboard_images/', null=True, blank=True, verbose_name="Rasm")

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name="Manzil")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name="Viloyat")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name="Tuman")
    address = models.CharField(max_length=255, verbose_name="Lokatsiya manzili", null=True, blank=True)

    latitude = models.FloatField(verbose_name="Latitude (kenglik)")
    longitude = models.FloatField(verbose_name="Longitude (uzunlik)")

    billboard_number = models.CharField(max_length=50, verbose_name="Billboard raqami")
    format = models.CharField(max_length=50, verbose_name="Format (masalan: 15FT)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free', verbose_name="Status")

    client = models.CharField(max_length=255, null=True, blank=True, verbose_name="Mijoz")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi", null=True, blank=True)
    expiry_date = models.DateField(verbose_name="Ijara tugash sanasi", null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Umumiy summa", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.billboard_number} - {self.location}"

    class Meta:
        verbose_name = "Billboard"
        verbose_name_plural = "Billboardlar"
