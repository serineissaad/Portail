from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Domaine(models.Model):
    nom_domaine = models.CharField(max_length=100, choices=[
        ('Santé', 'Santé'),
        ('Pollution', 'Pollution'),
        ('Environnementale', 'Environnementale'),
        ('Hybride', 'Hybride'),
    ])
    def __str__(self):
        return self.nom_domaine

class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=255)
    def __str__(self):
        return self.nom_categorie

class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class Localite(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

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
    def __str__(self):
        return self.format

class Ressource(models.Model):
    titre = models.CharField(max_length=255)
    lien_acces = models.CharField(max_length=255)
    description = models.TextField()
    description_auteurs = models.TextField(blank=True, null=True)
    description_localite = models.TextField(blank=True, null=True)
    protocole_collecte = models.TextField(blank=True, null=True)
    frequence_maj = models.CharField(max_length=100, blank=True, null=True)
    documentation = models.TextField(blank=True, null=True)
    licence = models.BooleanField()
    disponibilite = models.TextField(blank=True, null=True)
    nb_bd = models.IntegerField()
    from_year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2050)], blank=True, null=True)
    to_year = models.IntegerField(validators=[MinValueValidator(1950), MaxValueValidator(2050)], blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    domaines = models.ManyToManyField(Domaine)
    categories = models.ManyToManyField(Categorie, related_name='ressources')
    auteurs = models.ManyToManyField(Auteur, related_name='ressources')
    localites = models.ManyToManyField(Localite)
    formats = models.ManyToManyField(Format)
    def __str__(self):
        return self.titre

class LienAccesUtile(models.Model):
    description_lien = models.CharField(max_length=255, blank=True, null=True)
    lien = models.CharField(max_length=255)
    ressource = models.ForeignKey(Ressource, related_name='liens_utiles', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ressource.titre} - {self.lien}"
class BD_Reliee(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.ManyToManyField(Auteur, related_name='bd_reliees', blank=True)
    description = models.TextField(blank=True, null=True)
    nombre = models.IntegerField(blank=True, null=True)
    annee = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1950), MaxValueValidator(2050)])
    contact = models.CharField(max_length=255, blank=True, null=True)
    ressource = models.ForeignKey(Ressource, related_name='bd_reliees', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ressource.titre} - {self.titre}"