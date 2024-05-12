from django.db import models
from django.contrib.auth.models import User #django already has some table for user this table will have username,email,password etc(built-in user models)
# Create your models here.




class Task(models.Model):
    #attributes
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #when the user click delete the value will be deleted from the database too.
    title= models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    complete=models.BooleanField(default=False)
    create=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    class Meta:
        ordering=['complete']   #the completed task should be go to the bottom
