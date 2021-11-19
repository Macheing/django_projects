# https://docs.python.org/3/library/csv.html
# https://django-extensions.readthedocs.io/en/latest/runscript.html
# python manage.py runscript unesco_load

import csv
from unesco.models import Site, Category, State, Region, Iso

def run():
    file_handler = open('unesco/unesco_data.csv')
    file_reader = csv.reader(file_handler)
    next(file_reader)

    # iniatize related databases.
    Site.objects.all().delete()
    Category.objects.all().delete()
    State.objects.all().delete()
    Region.objects.all().delete()
    Iso.objects.all().delete()

    # columns format
    #|name|description|justification|year|longitude|latitude|area_hectares|category|state|region|iso|

    # loop through the data.
    for row in file_reader:
        print(row)
        try:
            y = float(row[6])
        except:
            y = None

        c, created = Category.objects.get_or_create(name=row[7])
        st,created = State.objects.get_or_create(name=row[8])
        r,created = Region.objects.get_or_create(name=row[9])
        i,created = Iso.objects.get_or_create(name=row[10])

        #clean unwanted characters e.g <p></p>, <em></em>
        des = row[1].replace('<p>',' ').replace('<em>',' ').replace('</em>',' ').replace('</p>',' ')
        jus = row[2].replace('<p>',' ').replace('<em>',' ').replace('</em>',' ').replace('</p>',' ')
        s,created = Site.objects.get_or_create(name=row[0],description=des,justification=jus,year=int(row[3]),
                                                longitude=float(row[4]),latitude=float(row[5]),area_hectares=y,
                                                category=c,state=st,region=r,iso=i)

        s.save()




