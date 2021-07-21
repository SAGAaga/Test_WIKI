from django.db import models


# current version of the page


class Page(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title

# page versions


class Versions(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
