from django.db import models
from datetime import timedelta


class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_serial_no = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.machine_name
    

class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100, unique=True)
    material_name = models.CharField(max_length=100, blank=False)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(editable=False, default=0)

    #  OEE calculation
    unplanned_downtime = models.DurationField(default=timedelta()) 
    ideal_cycle_time = models.FloatField(default=0)  
    actual_output = models.IntegerField(default=0)  
    good_products = models.IntegerField(default=0)  
    total_products = models.IntegerField(default=0)  
    availability = models.FloatField(blank=True, null=True)
    performance = models.FloatField(blank=True, null=True)
    quality = models.FloatField(blank=True, null=True)
    oee = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.duration = duration_seconds / 3600
        self.calculate_oee()
        super(ProductionLog, self).save(*args, **kwargs)

    def calculate_availability(self):
        available_time = (self.end_time - self.start_time).total_seconds()
        uptime = available_time - self.unplanned_downtime.total_seconds()
        self.availability = (uptime / available_time) * 100

    def calculate_performance(self):
        available_operating_time = (self.end_time - self.start_time).total_seconds() - self.unplanned_downtime.total_seconds()
        self.performance = (self.ideal_cycle_time * self.actual_output / available_operating_time) * 100

    def calculate_quality(self):
        self.quality = (self.good_products / self.total_products) * 100

    def calculate_oee(self):
        self.calculate_availability()
        self.calculate_performance()
        self.calculate_quality()
        self.oee = (self.availability * self.performance * self.quality) / 10000  

    def __str__(self):
        return self.material_name

    