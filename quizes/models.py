from django.db import models
import random
# Create your models here.

DIFF_CSOICES = (
        ('easy','easy'),
        ('meduim','meduim'),
        ('hard','hard'),
    )

class Quizes(models.Model):
    name = models.CharField( max_length=150)
    topic = models.CharField( max_length=150)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_scored_to_pass = models.IntegerField(help_text="required score in %")
    diffculity = models.CharField( max_length=6 , choices=DIFF_CSOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    
    class Meta:
        verbose_name_plural = "Quizes"
    