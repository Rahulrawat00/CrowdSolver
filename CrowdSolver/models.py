from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Member(models.Model):
    TYPE_OWNER = 'OWNER'
    TYPE_RENTER  = 'RENTER'
    RESIDENT_TYPE = [
        (TYPE_OWNER, 'OWNER'),
        (TYPE_RENTER,'RENTER')
    ]
    memberName = models.CharField((""), max_length=50)
    memberMail = models.EmailField((""), max_length=254)
    memberContact = models.CharField((""), max_length=10)
    memberPassword = models.CharField((""), max_length=50)
    memberAddress = models.CharField((""), max_length=50)
    memberImage = models.FileField((""), upload_to=None, max_length=100)
    memberType = models.CharField((""), max_length=50 ,choices=RESIDENT_TYPE, default=TYPE_OWNER )



    def __str__(self):
        return self.memberName
    

class Secretary(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Categoryname(models.Model):
    category = models.CharField(("category name"), max_length=50)
    def __str__(self):
        return self.category


class Issue(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    location_type = models.CharField(max_length=20)
    block = models.CharField(max_length=10)
    floor = models.IntegerField()
    flat_number = models.CharField(max_length=20, null=True, blank=True)
    attachment = models.FileField(upload_to='issues/', null=True, blank=True)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categoryname, on_delete=models.CASCADE,)
    member=models.ForeignKey(Member,  on_delete=models.CASCADE, null=True,blank=True, related_name='issues')

    def __str__(self):
        return self.title
    
class Solutions(models.Model):
    Issue_details = models.ForeignKey(Issue, verbose_name=(""), on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(("Title"), max_length=50)
    Description= models.TextField(("Description"))
    
    approve_count = models.IntegerField(default=0)
    reject_count = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)


class Vote(models.Model):
    solution = models.ForeignKey(Solutions, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('solution', 'member')



# class Categoryname(models.Model):

