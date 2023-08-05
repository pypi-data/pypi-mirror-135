from django.forms import ModelForm
from .models import Province, District, Municipality

class ProvinceForm(ModelForm):
    class Meta:
        model = Province
        fields = ['name']

class DistrictForm(ModelForm):
    class Meta:
        model = District
        fields = ['name', 'province']

class MunicipalityForm(ModelForm):
    class Meta:
        model = Municipality
        fields = ['name', 'district']
