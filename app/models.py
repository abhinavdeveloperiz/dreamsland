from django.db import models
from django.contrib.auth.models import User

# Customer Model
class Customer(User):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="customer_profiles", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

# Agent Model(created by the admin)
class Agent(models.Model):
    profile_picture = models.ImageField(upload_to="Agent_profile")
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # So admin can activate/deactivate agent


    def __str__(self):
        return self.user_name

class Property_category(models.Model):
    name = models.CharField(max_length=200)

class District(models.Model):
    name = models.CharField(max_length=100)

class City(models.Model):
    name = models.CharField(max_length=200)

# Property Model
class Property(models.Model):
    price = models.DecimalField(max_digits=12, decimal_places=2)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="district_obj")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city_obj")
    address = models.CharField(max_length=400)
    sqft = models.IntegerField()
    bhk = models.IntegerField()
    category = models.ForeignKey(Property_category, on_delete=models.CASCADE, related_name="category_obj")
    year_of_construction = models.IntegerField()
    images1 = models.ImageField(upload_to="property_images")
    images2 = models.ImageField(upload_to="property_images")
    images3 = models.ImageField(upload_to="property_images")
    images4 = models.ImageField(upload_to="property_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    sold_out = models.BooleanField(default=False)
    admin_approval = models.BooleanField(default=False)  # Manager approval for posting

    def __str__(self):
        return self.address

# Lead Model
class Leads(models.Model):
    customer_obj = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_obj")
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_obj")
    assign_to = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="lead_assignments")
    leads_choice = (
        ("cold", "cold"),
        ("warm", "warm"),
        ("hot", "hot"),
    )
    lead_status = models.CharField(max_length=100, choices=leads_choice)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead for {self.property_obj.address} ({self.lead_status})"

    # Method to auto-assign leads based on location
    @classmethod
    def assign_lead_based_on_location(cls, customer_location):
        # Example logic to assign leads based on location
        agents_in_location = Agent.objects.filter(location=customer_location)
        if agents_in_location.exists(): 
            return agents_in_location.first()  # Assign the first available agent
        return None  # Or return a fallback agent if needed

# Task Model
class Tasks(models.Model):
    assign_to = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="task_assign")
    deadline = models.DateTimeField()
    description = models.TextField()
    status_choice = (
        ("Not accepted", "Not accepted"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
    )
    task_status = models.CharField(max_length=200, choices=status_choice, default="Not accepted")

    def __str__(self):
        return f"Task for {self.assign_to.user_name} - {self.task_status}"

# Sales Model
class Sales(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent_sales")
    property_obj = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="sales_property")
    customer_obj = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales_customer")
    sale_price = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale for {self.property_obj.address}"

# Commission Model
class Commission(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent_commission")
    percentage = models.FloatField()  # e.g., 10% commission
    commission_amount = models.FloatField()

    def __str__(self):
        return f"Commission for {self.agent.user_name}"

# Account Balance Model
class AccountBalance(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent_account")
    total_sales = models.FloatField()
    commission_earned = models.FloatField()
    balance = models.FloatField()  # This can be updated based on sales and commission

    def __str__(self):
        return f"Balance for {self.agent.user_name}"
