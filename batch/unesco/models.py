from django.db import models

# Create your models here.

# Site data model
class Site(models.Model):
    name = models.CharField(max_length = 2600)
    description = models.CharField(max_length = 10000)
    justification = models.CharField(max_length = 10000)
    year = models.IntegerField(null = True)
    longitude = models.IntegerField(null = True)
    latitude = models.IntegerField(null = True)
    area_hectares = models.IntegerField(null = True)

    # foreign keys sections
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    iso = models.ForeignKey('Iso', on_delete=models.CASCADE)

    # show the name of site in admin view.
    def __str__(self):
        return self.name

# Category data model
class Category(models.Model):
    name = models.CharField(max_length = 200)

    # show the name of category in admin view.
    def __str__(self):
        return self.name

# State data model
class State(models.Model):
    name = models.CharField(max_length = 2000)

    # show the name of state in admin view.
    def __str__(self):
        return self.name

# Region data model
class Region(models.Model):
    name = models.CharField(max_length = 2000)

    # show the name of Region in admin view.
    def __str__(self):
        return self.name

# Iso data model
class Iso(models.Model):
    name = models.CharField(max_length = 128)

    # show the name of Iso in admin view.
    def __str__(self):
        return self.name

