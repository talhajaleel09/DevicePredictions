from django.db import models

class Device(models.Model):
    battery_power = models.IntegerField()
    blue = models.IntegerField(null=True)
    clock_speed = models.FloatField(null=True)
    dual_sim = models.IntegerField(null=True)
    fc = models.IntegerField(null=True)
    four_g = models.IntegerField(null=True)
    int_memory = models.IntegerField(null=True)
    m_dep = models.FloatField(null=True)
    mobile_wt = models.IntegerField(null=True)
    n_cores = models.IntegerField(null=True)
    pc = models.IntegerField(null=True)
    px_height = models.IntegerField(null=True)
    px_width = models.IntegerField(null=True)
    ram = models.IntegerField(null=True)
    sc_h = models.IntegerField(null=True)
    sc_w = models.IntegerField(null=True)
    talk_time = models.IntegerField(null=True)
    three_g = models.IntegerField(null=True)
    touch_screen = models.IntegerField(null=True)
    wifi = models.IntegerField(null=True)
    price_range = models.IntegerField(null=True)

    def __str__(self):
        return f"Mobile {self.id}"