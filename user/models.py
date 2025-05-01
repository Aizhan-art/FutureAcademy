from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from .choices import ROLE_CHOICES


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=223)
    last_name = models.CharField(max_length=223)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=223)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    grade = models.PositiveSmallIntegerField(blank=True, null=True)
    avatar = models.ImageField(upload_to='media/user_cover', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='user_children')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.is_admin = None

    def __str__(self):
        return self.last_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
