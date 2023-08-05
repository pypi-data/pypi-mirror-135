import uuid

from django.core.management.base import BaseCommand

from urlid_graph.models import Entity


class Command(BaseCommand):
    help = "Create Brasil.IO entities"

    def handle(self, *args, **options):
        brasilio_base_url = "https://id.brasil.io/"
        version = 1
        for name in ("company", "person", "candidacy", "court-case"):
            url = f"{brasilio_base_url}{name}/v{version}/"
            row = {
                "base_url": brasilio_base_url,
                "name": name,
                "version": version,
                "uuid": uuid.uuid5(uuid.NAMESPACE_URL, url),
            }
            obj = Entity.objects.filter(**row).first()
            created = False
            if obj is None:
                obj = Entity(**row)
                obj.save()
                created = True
            print(f"{'CREATED' if created else 'ALREADY EXISTS'} {name}, uuid = {obj.uuid}")
