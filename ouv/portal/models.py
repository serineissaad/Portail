from django.db import models

from django.db import models

class Domaine(models.Model):
    nom_domaine = models.CharField(max_length=100, choices=[
        ('Santé', 'Santé'),
        ('Pollution', 'Pollution'),
        ('Environnementale', 'Environnementale'),
        ('Hybride', 'Hybride'),
    ])

class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=255)

class Auteur(models.Model):
    nom = models.CharField(max_length=100)

class Localite(models.Model):
    nom = models.CharField(max_length=100)

class Format(models.Model):
    format = models.CharField(max_length=50, choices=[
        ('csv', 'csv'),
        ('xml', 'xml'),
        ('excel', 'excel'),
        ('json', 'json'),
        ('png', 'png'),
        ('vis', 'vis'),
        ('tsv', 'tsv'),
    ])

class Ressource(models.Model):
    titre = models.CharField(max_length=255)
    lien_acces = models.CharField(max_length=255)
    description = models.TextField()
    description_auteurs = models.TextField()
    description_localite = models.TextField()
    protocole_collecte = models.TextField()
    frequence_maj = models.CharField(max_length=100)
    documentation = models.TextField()
    licence = models.BooleanField()
    disponibilite = models.TextField()
    nb_bd = models.IntegerField()
    from_year = models.IntegerField()
    to_year = models.IntegerField()
    contact = models.CharField(max_length=255)
    domaines = models.ManyToManyField(Domaine)
    categories = models.ManyToManyField(Categorie, related_name='ressources')
    auteurs = models.ManyToManyField(Auteur, related_name='ressources')
    localites = models.ManyToManyField(Localite)
    formats = models.ManyToManyField(Format)

class LienAccesUtile(models.Model):
    description_lien = models.CharField(max_length=255)
    lien = models.CharField(max_length=255)
    ressource = models.ForeignKey(Ressource, related_name='liens_utiles', on_delete=models.CASCADE)

class BD_Reliee(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.ManyToManyField(Auteur, related_name='BD_Reliee')
    description = models.TextField()
    nombre = models.IntegerField()
    annee = models.IntegerField()
    contact = models.CharField(max_length=255)
    ressource = models.ForeignKey(Ressource, related_name='bd_reliees', on_delete=models.CASCADE)
