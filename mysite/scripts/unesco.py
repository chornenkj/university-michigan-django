import csv
import os
from mysite import settings
from unesco.models import Site, Category, State, Iso, Region

def create_db_file_from_csv():
    # read csv-file
    file_name = os.path.join(settings.BASE_DIR,'site/unesco/unesco.csv')
    file_cats = open(file_name,'r')
    reader = csv.reader(file_cats)
    # pass header
    next(reader)

    # delete all objects from
    Site.objects.using('unesco').all().delete()
    Category.objects.using('unesco').all().delete()
    State.objects.using('unesco').all().delete()
    Iso.objects.using('unesco').all().delete()
    Region.objects.using('unesco').all().delete()

    # File format: name - 0, description - 1, justification - 2, year - 3,
    # longitude - 4, latitude - 5, area_hectares - 6, category - 7,
    # state - 8, region - 9, iso - 10

    # read from reader and save to database
    for row in reader:
        row_category, created = Category.objects.using('unesco').get_or_create(name=row[7])
        row_state, created = State.objects.using('unesco').get_or_create(name=row[8])
        row_iso, created = Iso.objects.using('unesco').get_or_create(name=row[10])
        row_region, created = Region.objects.using('unesco').get_or_create(name=row[9])

        # validating values of year, longitude, latitude and area_hectares
        try:
            row_year = int(row[3])
        except:
            row_year = None
        try:
            row_longitude = float(row[4])
        except:
            row_longitude = None
        try:
            row_latitude = float(row[5])
        except:
            row_latitude = None
        try:
            row_area_hectares = float(row[6])
        except:
            row_area_hectares = None

        row_site, created = Site.objects.using('unesco').get_or_create(
            name=row[0],
            description=row[1],
            justification=row[2],
            year=row_year,
            longitude=row_longitude,
            latitude=row_latitude,
            area_hectares=row_area_hectares,
            category=row_category,
            state=row_state,
            region=row_region,
            iso=row_iso
        )