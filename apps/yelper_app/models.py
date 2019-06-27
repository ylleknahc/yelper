from django.db import models
from ..login_registration_app.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RestaurantManager(models.Manager):
    def new(self, postData, user):
        name = postData["name"]
        location = postData["location"]
        description = postData["description"]

        Restaurant.objects.create(name=name,
                                location=location,
                                description=description,
                                added_by=user)

    def validator(self, postData):
        name = postData["name"]
        location = postData["location"]
        description = postData["description"]

        errors = {}
        if not name:
            errors["name"] = "Name cannot be blank"
        elif len(name) < 2:
            errors["name"] = "Name should be at least 2 characters long"
        if not location:
            errors["location"] = "Location cannot be blank"
        if not description:
            errors["description"] = "Description cannot be blank"
        elif len(description) < 5:
            errors["description"] = "Description should be at least 5 characters long"
        return errors

class Restaurant(BaseModel):
    name = models.CharField(max_length=60)
    location = models.CharField(max_length=45)
    description = models.TextField()
    added_by = models.ForeignKey(User, related_name="restaurants", on_delete=models.CASCADE)
    objects = RestaurantManager()

class Review(BaseModel):
    content = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="reviews", on_delete=models.CASCADE)

class Comment(BaseModel):
    content = models.TextField()
    commenter = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name="comments", on_delete=models.CASCADE)

class Like(BaseModel):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="comments", on_delete=models.CASCADE)

class Favorite(BaseModel):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="favorites", on_delete=models.CASCADE)