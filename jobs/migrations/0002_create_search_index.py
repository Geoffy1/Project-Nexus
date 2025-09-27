from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [("jobs", "0001_initial")]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;"),
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS job_search_idx ON jobs_job USING gin (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,'')));"
        ),
    ]

