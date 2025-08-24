from django.db import migrations
from django.utils.text import slugify

def forwards_func(apps, schema_editor):
    Project = apps.get_model("api", "Project")
    Tag = apps.get_model("api", "Tag")
    db_alias = schema_editor.connection.alias

    for project in Project.objects.using(db_alias).all():
        if hasattr(project, 'technologies') and project.technologies:
            technologies_str = project.technologies
            tech_names = [name.strip() for name in technologies_str.split(',') if name.strip()]
            for tech_name in tech_names:
                tag, created = Tag.objects.using(db_alias).get_or_create(
                    name=tech_name,
                    defaults={'slug': slugify(tech_name)}
                )
                project.tags.add(tag)

def backwards_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0004_tag_post_tags_project_tags'),
    ]
    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]