import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript cats_load

from cats.models import Cat, Breed

def run():
    fhand = open('cats/meow.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Cat.objects.all().delete()
    Breed.objects.all().delete()

    # Name,Breed,Weight
    # Abby,Sphinx,6.4
    # Annie,Burmese,7.6
    # Ash,Manx,7.8
    # Athena,Manx,8.9
    # Baby,Tabby,6.9

    for row in reader:
        #row = str(row).replace("'","")
        print(row)
        #row = (row)

        b, created = Breed.objects.get_or_create(name=row[1])
        w = float(row[2])
        c = Cat(nickname=row[0], breed=b, weight=w)
        c.save()
