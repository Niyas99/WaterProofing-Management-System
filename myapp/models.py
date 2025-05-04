from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class dealers_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    id_proof_number = models.BigIntegerField()
    image = models.FileField()

class administrative_staff_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    id_proof_number = models.BigIntegerField()
    image = models.FileField()

class product_table(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.FileField()

class workers_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    email = models.CharField(max_length=100)
    skills = models.TextField()
    availability = models.CharField(max_length=100)
    image = models.FileField()
    id_proof_number = models.BigIntegerField()

class complaint_table(models.Model):
    DEALEARS = models.ForeignKey(dealers_table,on_delete=models.CASCADE)
    description = models.TextField()
    replay = models.CharField(max_length=100)
    date = models.DateField()

class feedback_table(models.Model):
    DEALEARS = models.ForeignKey(dealers_table, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product_table, on_delete=models.CASCADE)
    comments = models.TextField()
    rating = models.IntegerField()

    date = models.DateField()

class job_request_table(models.Model):
    DEALEARS = models.ForeignKey(dealers_table, on_delete=models.CASCADE)
    work = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    # amount = models.IntegerField()

class purchase_request_table(models.Model):
    DEALEARS = models.ForeignKey(dealers_table, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.IntegerField()


class purchase_request_more_table(models.Model):
    PURCHASE = models.ForeignKey(purchase_request_table,on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product_table,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.IntegerField()

class allocate_work(models.Model):
    JOB_REQUEST = models.ForeignKey(job_request_table,on_delete=models.CASCADE)
    WORKER = models.ForeignKey(workers_table,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    allocation_date = models.DateField()
    status = models.CharField(max_length=100)

class payment(models.Model):

    PURCHASE_REQUEST_TABLE = models.ForeignKey(purchase_request_table,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100)


