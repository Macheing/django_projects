
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

# Make db model
class Make(models.Model):
    name = models.CharField(
            max_length=200,
            help_text='Enter a Maker or Manufacturer (e.g. Dodge)',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")]
    )
    # convert all entries to db objects
    def __str__(self):
        """String for representing the Model object."""
        return self.name

# Auto db model
class Auto(models.Model):
    nickname = models.CharField(
            max_length=200,
            help_text = 'Enter Brand name of a car (e.g toyota hilux)',
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")]
    )

    make = models.ForeignKey('Make', on_delete=models.CASCADE, null=False)
    mileage = models.PositiveIntegerField()
    comments = models.CharField(max_length=300)

    # Shows up in the admin list
    def __str__(self):
        return self.nickname

