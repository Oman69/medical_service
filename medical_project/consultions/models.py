from django.db import models


class Consultation(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Подтверждена'),
        ('waiting', 'Ожидает'),
        ('started', 'Начата'),
        ('completed', 'Завершена'),
        ('paid', 'Оплачена'),
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name='Статус')

    doctor = models.ForeignKey('users.Doctor', on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='consultations')
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE, related_name='consultations')

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'
        ordering = ['-created_date']

    def __str__(self):
        return f"Консультация {self.patient} с {self.doctor} - {self._status}"

    def _status(self):
        return self.status
