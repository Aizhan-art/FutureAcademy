from django.db import models

class TaskStatusEnum(models.TextChoices):
    PENDING = 'pending', 'В ожидании'
    IN_PROGRESS = 'in_progress', 'В процессе'
    COMPLETED = 'completed', 'Завершено'


class DiaryGradeEnum(models.IntegerChoices):
    A_PLUS = 5, 'Отлично'
    A = 4, 'Хорошо'
    B = 3, 'Удовлетворительно'
    C = 2, 'Неудовлетворительно'