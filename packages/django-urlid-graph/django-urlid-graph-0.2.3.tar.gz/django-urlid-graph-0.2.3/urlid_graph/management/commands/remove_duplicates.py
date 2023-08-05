import psycopg2
from django.core.management.base import BaseCommand

from urlid_graph import settings as urlid_graph_settings
from urlid_graph.utils import remove_duplicates_sql, working
from urlid_graph.models import Object, Property


class Command(BaseCommand):
    help = "Remove duplicates from Object and Property tables"

    def add_arguments(self, parser):
        parser.add_argument("--disable-autovacuum", action="store_true")
        parser.add_argument("--disable-indexes", action="store_true")

    def handle(self, *args, **options):
        disable_autovacuum = options["disable_autovacuum"]
        disable_indexes = options["disable_indexes"]

        connection = psycopg2.connect(urlid_graph_settings.DJANGO_DATABASE_URL)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        with working("Removing duplicates from Object"), connection.cursor() as cursor:
            queries = remove_duplicates_sql(
                table_name=Object._meta.db_table,
                field_names=("uuid", "entity_uuid", "internal_id"),
                disable_autovacuum=disable_autovacuum,
                disable_indexes=disable_indexes,
                disable_sync_commit=True,
                disable_triggers=True,
            )
            for query in queries:
                cursor.execute(query)

        with working("Removing duplicates from Property"), connection.cursor() as cursor:
            queries = remove_duplicates_sql(
                table_name=Property._meta.db_table,
                field_names=("object_uuid", "value_type", "name", "source", "value", "value_datetime"),
                disable_autovacuum=disable_autovacuum,
                disable_indexes=disable_indexes,
                disable_sync_commit=True,
                disable_triggers=True,
            )
            for query in queries:
                cursor.execute(query)
