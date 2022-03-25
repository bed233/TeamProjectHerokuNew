from django.db import models


class DashboardModel(models.Model):
    name = models.CharField(max_length=100, default="Table_Number")
    selected_table_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
