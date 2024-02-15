from django.db import models
from django.core.validators import MinValueValidator


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True, default='example@example.com')
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    timings_from = models.DateTimeField()
    timings_to = models.DateTimeField()

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    workout_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True, default='example@example.com')
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField()
    weight = models.FloatField()
    waist_measurement = models.FloatField()
    BMI = models.FloatField()
    goal = models.CharField(max_length=100)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class FeeReport(models.Model):
    fee_report_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date_paid = models.DateField()
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Fee Report #{self.fee_report_id}"

class SalaryReport(models.Model):
    salary_report_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date_paid = models.DateField()

    def __str__(self):
        return f"Salary Report #{self.salary_report_id}"

class ExpensesReport(models.Model):
    expense_report_id = models.AutoField(primary_key=True)
    TYPE_CHOICES = [
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('supplies', 'Supplies'),
        ('others', 'Others')
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date_paid = models.DateField()

    def __str__(self):
        return f"Expense Report #{self.expense_report_id}"

from django.db import models
from django.core.validators import MinValueValidator

class ProfitReport(models.Model):
    profit_report_id = models.AutoField(primary_key=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    expenses = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    profit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], editable=False)
    date = models.DateField()

    def __str__(self):
        return f"Profit Report #{self.profit_report_id}"

    def save(self, *args, **kwargs):
        self.profit = self.income - self.expenses
        super().save(*args, **kwargs)


class ProgressReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2)
    cardiovascular_endurance = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    flexibility = models.PositiveIntegerField()
    other_metrics = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Progress Report for {self.customer.name} on {self.date}"
