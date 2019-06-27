from django.db import models
# from django.core.validators import EmailValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime

import bcrypt

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class UserManager(models.Manager):
    def fetch_user(self, postData):
        email = postData['email']
        user = User.objects.get(email=email)
        return user

    def create_user(self, postData):
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        password = postData['password']
        confirm_password = postData['confirm_password']
        birthday = postData['birthday']

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password_hash.decode(),
                                    birthday=birthday)
        return user

    def validate_registration(self, postData):
        errors = {}

        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        password = postData['password']
        confirm_password = postData['confirm_password']
        birthday = postData['birthday']

        if not first_name:
            errors['first_name'] = "First Name should not be blank"
        else:
            if len(first_name) < 2:
                errors['first_name'] = "First Name should be at least 2 characters"
            if not first_name.isalpha():
                errors['first_name'] = "First Name should only contain letters"
        if not last_name:
            errors['last_name'] = "Last Name should not be blank"
        else:
            if len(last_name) < 2:
                errors['last_name'] = "Last Name should be at least 2 characters"
            if last_name.isalpha() == False:
                errors['last_name'] = "Last Name should only contain letters"
        if not email:
            errors['email'] = "Email should not be blank"
        else:
            try:
                validate_email(email)
                print("True")
            except ValidationError:
                errors['email'] = "Email should be a valid email address"
            if User.objects.filter(email=email).exists():
                errors['email'] = "Email already exists in the system"
        if not password:
            errors['password'] = "Password should not be blank"
        else:
            if len(password) < 8:
                errors['password'] = "Password should be at least 8 characters"
        if not confirm_password:
            errors['confirm_password'] = "Confirm Password should not be blank"
        else:
            if password != confirm_password:
                errors['password'] = "Password does not match"
                errors['confirm_password'] = "Password does not match"
        if not birthday:
            errors['birthday'] = "Birthday should not be blank"
        else:
            birthday = datetime.strptime(birthday, "%Y-%m-%d")
            today = datetime.now()
            if today < birthday:
                errors['birthday'] = "Birthday is not in the past"
            if today.year - birthday.year < 13:
                errors['birthday'] = "You are too young!"
        return errors

    def validate_login(self, postData):
        errors = {}

        email = postData['email']
        password = postData['password']

        if not email:
            errors['email'] = "Email should not be blank"
        else:
            try:
                validate_email(email)
                print("True")
            except ValidationError:
                errors['email'] = "Email should be a valid email address"
            if not User.objects.filter(email=email).exists():
                errors['email'] = "Email does not exist in the system"
            else:
                user = User.objects.get(email=email)
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors['password'] = "Password is incorrect"
        if not password:
            errors['password'] = "Password should not be blank"
        else:
            if len(password) < 8:
                errors['password'] = "Password should be at least 8 characters"
        return errors


class User(BaseModel):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=30)
    birthday = models.DateTimeField(null=True)
    objects = UserManager()
