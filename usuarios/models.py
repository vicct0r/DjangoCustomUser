from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid

from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email é um campo obrigatório!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField('Email', unique=True)
    nome_completo = models.CharField('Nome Completo', max_length=50)
    is_funcionario = models.BooleanField('Funcionário?', default=False)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'is_funcionario']

    objects = CustomUserManager()



class Aluno(models.Model):
    CHOICES = (
        ('BCC', 'Ciência da Computação'),
        ('ZO', 'Zootecnia'),
        ('AG', 'Agronomia'),
        ('QI', 'Quimica Industrial'),
    )
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    curso = models.CharField('Curso', max_length=3, choices=CHOICES)
    is_ativo = models.BooleanField('Ativo?', default=False, editable=False)
    matricula = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


    def save(self, *args, **kwargs):
        if self.curso:
            self.is_ativo = True
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.curso}'