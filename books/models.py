from django.db import models

# Shelf
class Shelfmodel(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id) + self.name

# Book
class Bookmodel(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField(null=True)
    num_pages = models.IntegerField(null=True)
    publication_year = models.IntegerField(null=True)
    average_rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# Review
class Reviewmodel(models.Model):
    book = models.ForeignKey(Bookmodel, on_delete=models.CASCADE)
    shelf = models.ManyToManyField(Shelfmodel)

    rating = models.FloatField(null=True)
    started_at = models.DateField(null=True)
    read_at = models.DateField(null=True)

    class Meta:
        ordering = ['read_at']

    def __str__(self):
        return str(self.started_at)

