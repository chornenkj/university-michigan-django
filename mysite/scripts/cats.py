import csv
import os
from mysite import settings
from cats.models import Breed, Cat

def refresh():
    # read csv-file
    file_name = os.path.join(settings.BASE_DIR,'site/cats/meow.csv')
    file_cats = open(file_name,'r')
    reader = csv.reader(file_cats)
    # pass header
    next(reader)

    # delete all objects from Cats and Breeds
    Cat.objects.all().delete()
    Breed.objects.all().delete()

    # read from reader and save to database
    for row in reader:
        b, created = Breed.objects.get_or_create(name=row[1])
        c = Cat(nickname=row[0],breed=b,weight=round(float(row[2])))
        c.save()