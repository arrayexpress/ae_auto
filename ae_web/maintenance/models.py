from django.db import models

# Create your models here.


STATUS = (
    ('P', 'Pending'),
    ('F', 'Finished'),
    ('E', 'Execution Error'),

)


class Validate(models.Model):
    job_id = models.CharField(null=False, unique=True, max_length=200)

    data_dir = models.CharField(null=True, max_length=200)
    validation_report = models.TextField(null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='P')



