from django.db import models

class InvestmentManagement(models.Model):
    profit = models.IntegerField(null=False)
    duration = models.IntegerField(null=False) 
    class Meta:
        db_table = "InvestmentManagement" 

class SignUpRequests(models.Model):
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    username = models.TextField(null=False)
    adress = models.TextField(null=False)
    number_phone = models.TextField(null=False)
    email = models.TextField(null=False)
    bank_name = models.TextField(null=False)
    bank_account = models.TextField(null=False)
    password = models.TextField(null=False, blank=True)
    front_identity_card = models.ImageField(null=False)
    back_identity_card = models.ImageField(null=False)
    date_of_request = models.DateField(null=False)
    class Meta:
        db_table = "SignUpRequests"

class InvestmentRequests(models.Model):
    username = models.TextField(null=False)
    amount_to_invest = models.FloatField(null=False)
    amount_to_get = models.FloatField(null=False)
    interest = models.FloatField(null=False)
    date_of_request = models.DateField(null=False)
    date_of_payment = models.DateField(null=False)
    class Meta:
        db_table = "InvestmentRequests"

class ApprovedSignUpRequests(models.Model):
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    username = models.TextField(null=False)
    adress = models.TextField(null=False)
    number_phone = models.TextField(null=False)
    email = models.TextField(null=False)
    bank_name = models.TextField(null=False)
    bank_account = models.TextField(null=False)
    password = models.TextField(null=False)
    front_identity_card = models.ImageField(null=False)
    back_identity_card = models.ImageField(null=False)
    class Meta:
        db_table = "ApprovedSignUpRequests" 

class ApprovedInvestmentRequests(models.Model):
    username = models.TextField(null=False)
    amount_to_invest = models.FloatField(null=False)
    amount_to_get = models.FloatField(null=False)
    interest = models.FloatField(null=False)
    date_of_investment = models.DateField(null=False)
    date_of_payment = models.DateField(null=False)
    status = models.TextField(null=False)
    class Meta:
        db_table = "ApprovedInvestmentRequests" 

class PaymentCompleted(models.Model):
    username = models.TextField(null=False)
    amount_paid = models.FloatField(null=False)
    interest_paid = models.FloatField(null=False)
    date_of_payment = models.DateField(null=False)
    class Meta:
        db_table = "PaymentCompleted" 

class TopInvestors(models.Model):
    username = models.TextField(null=False)
    amount_invested = models.FloatField(null=False)
    net_profit = models.FloatField(null=False)
    class Meta:
        db_table = "TopInvestors"     

