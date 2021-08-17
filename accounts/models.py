from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken



class UserAccountManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,   **extra_fields)

        user.set_password(password)
        user.save()

        return user
    def create_superuser(self,email,username, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email,username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
    
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class TypeAbonn(models.TextChoices):
    Etudiant = 'Et', ('Etudiant')
    Enseignant = 'En', ('Enseignant')
    Admin = 'Admin', ('Administrateur')
class Abonne(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField ( verbose_name = "email" , unique = True )
    username = models.CharField ( max_length = 60 , unique = True )
    # date_joined = models.DateTimeField ( verbose_name = "date joined" , auto_now_add = True )
    is_admin = models.BooleanField ( default = False )
    is_active = models.BooleanField ( default = True )
    is_staff = models.BooleanField ( default = False )
    is_superuser = models.BooleanField ( default = False )
    date_de_naissance = models.DateField ()
    numero_de_tel = models.IntegerField ()
    type = models.CharField ( max_length = 20 ,
                              choices = TypeAbonn.choices ,
                              default = TypeAbonn.Etudiant , )

    
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']


    
    def __str__(self):
        return self.email
    
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



