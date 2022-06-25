from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from datetime import datetime
from io import BytesIO
import os.path
import uuid
from django.contrib.auth.models import User

# Max size of image file
MAX_UPLOAD_SIZE = 5242880
ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS


class PostManager(models.Manager):
    def new_thread(self, post_data, file_data):

        errors = []


        if "image" not in file_data:
            errors.append("You must upload an image to start a thread")
        elif file_data["image"].name.find(".") == -1:
            errors.append("Image must be '.jpg', '.jpeg', '.gif', or '.png'")
        elif file_data["image"].name.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
            errors.append("Image must be '.jpg', '.jpeg', '.gif', or '.png'")
        elif file_data["image"].size > MAX_UPLOAD_SIZE:
            errors.append("Image must 5MB or less in size")

        print(dir(file_data["image"]))

        if len(post_data["subject"]) < 1:
            errors.append("You must include a subject to start a thread")
        elif len(post_data["subject"]) < 3:
            errors.append("Subject must be 3 characters or more")

        if len(errors) < 1:
            file_name = file_data["image"].name
            file_data["image"].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])

            return Post.objects.create(
                subject=post_data["subject"],
                name="Anonymous" if len(post_data["name"]) == 0 else post_data["name"],
                email=post_data["email"],
                comment=post_data["comment"],
                file_name=file_name,
                image=file_data["image"],
                is_thread=True,
                is_sage=False
            )
        else:
            return errors

    def new_reply(self, post_data, file_data, post_id):

        errors = []

        if "image" not in file_data and len(post_data["comment"]) < 1:
            errors.append("You must reply with an image or a comment")
        elif "image" not in file_data and len(post_data["comment"]) < 2:
            errors.append("Comment must be 2 characters or more")
        
        if "image" in file_data:
            if file_data["image"].name.find(".") == -1:
                errors.append("Image must be '.jpg', '.jpeg', '.gif', or '.png'")
            elif file_data["image"].name.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
                errors.append("Image must be '.jpg', '.jpeg', '.gif', or '.png'")
            else:
                file_name = file_data["image"].name
                file_data["image"].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])

        if len(errors) < 1:
            post = Post.objects.create(
                name="Anonymous" if len(post_data["name"]) == 0 else post_data["name"],
                email=post_data["email"],
                comment=post_data["comment"],
                file_name=None if "image" not in file_data else file_name,
                image=None if "image" not in file_data else file_data["image"],
                is_thread=False,
                is_sage=post_data["email"].lower() == "sage"
            )
            thread = Post.objects.get(id=post_id)
            thread.replies.add(post)
            if not post.is_sage:
                thread.updated_at = datetime.now()
                thread.save()
            return post
        else:
            return errors


class Post(models.Model):
    subject = models.CharField(max_length=228, default=None, blank=True, null=True)
    name = models.CharField(max_length=54)
    email = models.CharField(max_length=154)
    comment = models.TextField(max_length=2000)
    file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    image = models.FileField(upload_to='bchan/', default='bchan/default.jpg', blank=True, null=True)
    is_thread = models.BooleanField()
    is_sage = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replies = models.ManyToManyField("self", blank=True, related_name="thread")
    objects = PostManager()