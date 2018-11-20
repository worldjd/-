from django.db import models


class User(models.Model):
    sex_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密"),
    )
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=20, null=True)
    sex = models.SmallIntegerField(choices=sex_choices, default=3)
    school = models.CharField(max_length=20, null=True)
    home = models.CharField(max_length=20, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    revise_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.mobile, self.password