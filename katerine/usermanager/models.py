from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .semac_utils import FieldMaxLength


class SemacUserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **other_fields)


class SemacUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=FieldMaxLength.EMAIL, primary_key=True, blank=False, null=False)
    is_email_authenticated = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    object = SemacUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'Email: {self.email} | is_staff: {self.is_staff} | is_superuser: {self.is_superuser}'


class UserPersonalData(models.Model):

    cpf = models.CharField(max_length=FieldMaxLength.CPF, primary_key=True, null=False, blank=False, unique=True)
    user_email = models.OneToOneField(SemacUser, on_delete=models.CASCADE, related_name='personal_data')
    full_name = models.CharField(max_length=FieldMaxLength.FULL_NAME, null=False, blank=False)
    dob = models.DateField(blank=False, null=False)
    state = models.CharField(max_length=FieldMaxLength.STATE, null=False, blank=False)
    city = models.CharField(max_length=FieldMaxLength.CITY, null=False, blank=False)
    address = models.CharField(max_length=FieldMaxLength.ADDRESS, null=False, blank=False)
    contact_number = models.CharField(max_length=FieldMaxLength.CONTACT_NUMBER, null=False, blank=False)

    def __str__(self):
        return f'CPF: {self.cpf} | Full Name: {self.full_name} | Email: {self.user_email}'


class UserUnespData(models.Model):

    ra = models.CharField(max_length=FieldMaxLength.RA, primary_key=True, null=False, blank=False, unique=True)
    user_cpf = models.OneToOneField(UserPersonalData, on_delete=models.CASCADE, related_name='unesp_data')
    course_name = models.CharField(max_length=FieldMaxLength.COURSE_NAME, null=False, blank=False)

    def __str__(self):
        return f'RA: {self.ra} | CPF: {self.user_cpf} | Course Name: {self.course_name}'


class Subscription(models.Model):

    id = models.AutoField(primary_key=True)
    user_cpf = models.OneToOneField(UserPersonalData, on_delete=models.CASCADE, related_name='subscription')
    type = models.CharField(max_length=FieldMaxLength.SUBSCRIPTION_TYPE, null=False, blank=False)
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id} | CPF: {self.user_cpf} | Type: {self.type} | Is Payed: {self.is_payed}'


class Lecturer(models.Model):

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=FieldMaxLength.FULL_NAME, null=False, blank=False)
    email = models.EmailField(max_length=FieldMaxLength.EMAIL, null=False, blank=False, unique=True)

    def __str__(self):
        return f'ID: {self.id} | Full Name: {self.full_name} | Email: {self.email}'


class Lecture(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=FieldMaxLength.LECTURE_TITLE, null=False, blank=False)
    lecturer_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='lecture')
    date_and_time = models.DateTimeField(blank=False, null=False)
    enable_presence_url = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id} | Title: {self.title} | Date and Time: {self.date_and_time}'


class PersonOnLecture(models.Model):

    id = models.AutoField(primary_key=True)
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='applied_lectures')
    user_cpf = models.ForeignKey(UserPersonalData, on_delete=models.CASCADE, related_name='participated_lectures')

    def __str__(self):
        return f'ID: {self.id} | Lecture ID {self.lecture_id} | User CPF: {self.user_cpf}'


class SemacUserAuthenticationCode(models.Model):

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=FieldMaxLength.AUTHENTICATION_CODE, null=False, blank=False)
    user_email = models.OneToOneField(SemacUser, on_delete=models.CASCADE, related_name='auth_code')

    def __str__(self):
        return f'Email: {self.user_email} | Code: {self.code}'
