from django.db import models




class Transaction(models.Model):
    

    ref = models.CharField(max_length=100, unique=True)  # tx_ref
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='NGN')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
  
    flutterwave_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
    

class Register(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(
        ('male', 'male'),
        ('female', 'female')
    ))
    branch = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    
    

