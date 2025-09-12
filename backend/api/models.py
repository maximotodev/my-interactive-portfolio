# backend/api/models.py
from django.db import models
from django.utils.text import slugify
# --- NEW TAG MODEL ---
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if this is your current position")
    responsibilities = models.TextField(help_text="Enter each responsibility on a new line. They will be formatted as bullet points.")
    
    class Meta:
        ordering = ['-start_date'] # Show newest jobs first

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=100, default="Coursera")
    credential_url = models.URLField(blank=True, null=True)
    date_issued = models.DateField()

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # technologies = models.CharField(max_length=300, help_text="Comma-separated list of technologies")
    repository_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="A URL-friendly version of the title. Will be auto-generated.")
    content = models.TextField(help_text="Write your blog post content using Markdown.")
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email}) re: {self.subject}"

class Stall(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    merchant_pubkey = models.CharField(max_length=64, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=10)
    shipping_zones = models.JSONField(default=list)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list)
    currency = models.CharField(max_length=10)
    price = models.FloatField()
    quantity = models.IntegerField(null=True, blank=True)
    specs = models.JSONField(default=list)
    shipping = models.JSONField(default=list)
    tags = models.JSONField(default=list) # To store 't' tags from the event
    event_id = models.CharField(max_length=64, unique=True, db_index=True) # To store the latest event hash
    merchant_pubkey = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
# class Listing(models.Model):
#     event_id = models.CharField(max_length=64, unique=True, db_index=True)
#     seller_pubkey = models.CharField(max_length=64, db_index=True)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price_sats = models.BigIntegerField(blank=True, null=True)
#     image_url = models.URLField(max_length=1024, blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title