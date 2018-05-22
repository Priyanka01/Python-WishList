from django.db import models
import bcrypt
from datetime import datetime

# User model manager
class UserManager(models.Manager):
    def validate_register(self, postdata):
        errors = {}
        name = postdata['name']
        username = postdata['username']
        password = postdata['pwd']
        confirm_pwd= postdata['confirm_pwd']
        datehired = postdata['datehired']

        if len(name) < 1:
            errors['name'] = "Name cannot be empty"

        if len(name) <= 3:
            errors['name'] = "Name should be more than 3 characters"
        
        if len(username) < 1:
            errors['username'] = "Username cannot be empty"

        if len(username) <= 3:
            errors['username'] = "Username should be more than 3 characters"
            
        elif User.objects.filter(username=username):
            errors['duplicateusername'] = "Username already used! Try different username"

        if len(password) < 1:
            errors['password'] = "Password cannot be empty"
        elif len(password) < 8:
            errors['password_len'] = "Password should be atleast 8 characters"
        
        if confirm_pwd != password:
            errors['confirm_pwd'] = "password not matched"

        if datehired > str(datetime.today()):
            errors['datehired'] = "Date Hired cannot be more than today's date"

        return errors

    # Register new user
    def insertuser(self,postdata):
        errors = {}
        message = self.validate_register(postdata)
        if message:
            return message
        else:
            pw_hash = bcrypt.hashpw(postdata['pwd'].encode(), bcrypt.gensalt())
            User.objects.create(name=postdata['name'],username=postdata['username'],datehired=postdata['datehired'], pwd=pw_hash)
            return {'user': User.objects.last()}

    # Validate login user
    def validate_login(self, postdata):
        errors = {}
        try:
            user = User.objects.get(username=postdata['loginusername'])
        except:
            errors['login'] = "invalid username"
            return errors
        
        if bcrypt.checkpw(postdata['loginpwd'].encode('utf-8'), user.pwd.encode('utf-8')):
            return {'user': user}
        else:
            errors['login'] = "invalid password"
            return errors

# Model - User
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length = 30)
    datehired = models.DateField()
    pwd = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# List model manager    
class ListManager(models.Manager):
    def validate_item(self, postdata):
        errors = {}
        item = postdata['item']
        if len(item) < 1:
            errors['item'] = "Item cannot be empty!!"
        elif len(item) <= 3 :
            errors['itemlen'] = "Item should be more than 3 characters!"
        return errors

    def createItem(self, postdata, userid):
        message = self.validate_item(postdata)
        if message:
            return message
        else:
            list_obj = List.objects.create(item=postdata['item'],user_created_item = User.objects.get(id=userid))
            list_obj.added_by_users.add(User.objects.get(id=userid))
            return {'list': List.objects.last()}
    
    def addItem(self, itemid, userid):
        List.objects.get(id = itemid).added_by_users.add(User.objects.get(id = userid))
        return {'success': 'Added to List!'}

    def removeItem(self, itemid, userid):
        List.objects.get(id = itemid).added_by_users.remove(User.objects.get(id = userid))
        return {'success': 'Removed from List!'}

#Model - List    
class List(models.Model):
    item = models.TextField()
    added_by_users = models.ManyToManyField(User, related_name = 'added_items')
    user_created_item= models.ForeignKey(User, related_name= 'items_created_by')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ListManager()



