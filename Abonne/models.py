from django.db import models

# Create your models here.
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from accounts.models import Abonne






class TypeAbonn(models.TextChoices):
    Etudiant = 'Et', ('Etudiant')
    Enseignant = 'En', ('Enseignant')
    Admin = 'Admin', ('Administrateur')





class Niveau(models.Model):
    nom_niveau = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.nom_niveau


class Matiere(models.Model):
    Nom_matiere = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, db_index=True)
    Niveau = models.ForeignKey(Niveau, related_name='matiers', on_delete=models.CASCADE)


class Enseignant ( Abonne ):
    Niveau = models.ManyToManyField ( Niveau )
    Matiere = models.ManyToManyField ( Matiere )


class Etudiant ( Abonne ):
    Niveau = models.ForeignKey ( Niveau , on_delete = models.CASCADE )


class Chapitre(models.Model):
    titre_chapitre = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, db_index=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class Document(models.Model):
    Chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre_doc = models.CharField(max_length=255)
    description_doc = models.ImageField(upload_to='images/')
    slug = models.CharField(max_length=255, db_index=True)


class Video(models.Model):
    Chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre_video = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, db_index=True)
    nb_like = models.IntegerField()
    nb_dislike = models.IntegerField()
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name="")
