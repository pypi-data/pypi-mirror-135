from django.db import models

# Create your models here.
class Province(models.Model):
    class Meta:
        db_table = "province"
        verbose_name_plural = "provinces"
        ordering = ['name']
    
    name = models.CharField(max_length=15, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def get_districts(self):
        return self.district_set.all()

class District(models.Model):
    class Meta:
        db_table = "district"
        verbose_name_plural = "districts"
        ordering = ['name']

    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    def get_province(self):
        return self.province
    
    def get_municipalities(self):
        return self.municipality_set.all()


class Municipality(models.Model):
    class Meta:
        db_table = "municipality"
        verbose_name_plural = "municipalities"
        ordering = ['name']

    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return self.name
    
    def get_district(self):
        return self.district

    def get_province(self):
        return self.get_district().province
