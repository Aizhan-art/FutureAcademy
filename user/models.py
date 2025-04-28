from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            phone_number=phone_number,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            username=username,
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
    grade = models.PositiveSmallIntegerField()
    avatar = models.ImageField(upload_to='media/user_cover', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    role = models.BooleanField()
    is_active = models.BooleanField(default=True)



    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

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


class OTP(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    if_used = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
