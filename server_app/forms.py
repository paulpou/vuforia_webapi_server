from django.forms import ModelForm
from .models import TargetData , TreasureHuntData , SearchTargetData


class TargetForm(ModelForm):
    class Meta:
        model = TargetData
        fields = ['target_name','target_recognition_image','target_image','target_text','target_3d_model','target_image']

class SearchTargetDataForm(ModelForm):
    class Meta:
        model = SearchTargetData
        fields = ['targetid']
