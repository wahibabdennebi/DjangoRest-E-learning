from rest_framework import serializers
from .models import Abonne
from .models import Niveau
from .models import Matiere
from .models import Chapitre
from .models import Video
from .models import Document
#______________________________________________________________________











#____________________________________________________________________
class MatierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class NiveauSerializer(serializers.ModelSerializer):
     matiers = MatierSerializer(many=True)

     class Meta :
            model= Niveau
            fields=['nom_niveau','slug','matiers']


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


