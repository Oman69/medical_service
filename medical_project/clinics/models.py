from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название клиники')
    legal_address = models.TextField(verbose_name='Юридический адрес')
    physical_address = models.TextField(verbose_name='Физический адрес')

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'

    def __str__(self):
        return self.name


class DoctorClinic(models.Model):
    doctor = models.ForeignKey('users.Doctor', on_delete=models.CASCADE, related_name='clinics')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')

    class Meta:
        verbose_name = 'Врач в клинике'
        verbose_name_plural = 'Врачи в клиниках'
        unique_together = ('doctor', 'clinic')

    def __str__(self):
        return f"{self.doctor} - {self.clinic}"