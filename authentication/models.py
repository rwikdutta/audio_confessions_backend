from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentModel(models.Model):
    name=models.CharField(max_length=256,null=True,blank=True)
    year=models.DecimalField(max_digits=1,decimal_places=0,choices=(
        (1,'1st year'),
        (2,'2nd Year'),
        (3,'3rd Year'),
        (4,'4th Year'),
     ),blank=False,null=False)
    dept=models.CharField(max_length=3,choices=(
        ('CSE','CSE'),
        ('IT', 'IT'),
        ('ECE', 'ECE'),
        ('EE', 'EE'),
        ('MCA', 'MCA'),
    ),blank=False,null=False)
    passout_year=models.DecimalField(max_digits=4,decimal_places=0,choices=(
        (2017, 2017),
        (2018,2018),
        (2019, 2019),
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
    ),blank=False,null=False)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False,null=False,blank=False)


