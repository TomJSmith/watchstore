from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Customer(models.Model):
	Email = models.EmailField(max_length=50, primary_key=True)
	Password = models.CharField(max_length=50)
	FName = models.CharField(max_length=50)
	LName = models.CharField(max_length=50)
	Address = models.CharField(max_length=200)
	def __str__(self):
		return self.Email
	
class Credit_Card(models.Model):
	Number = models.IntegerField(primary_key=True)
	FName = models.CharField(max_length=50)
	LName = models.CharField(max_length=50)
	Expiry_Date = models.DateField('Date (m/y)') # how to change datefield format or use something else
	Security_Code = models.IntegerField(default=0)
	CEmail = models.ForeignKey(Customer, on_delete=models.CASCADE)
	def __str__(self):
		return "%d" % self.Number
	
class Moderator(models.Model):
	HIGH = 'HI'
	MEDIUM = 'MED'
	LOW = 'LOW'
	RESP_CHOICE = ((HIGH, 'High'), (MEDIUM, 'Medium'), (LOW, 'Low'))
	Email = models.EmailField(max_length=50, primary_key=True)
	Password = models.CharField(max_length=50)
	FName = models.CharField(max_length=50)
	LName = models.CharField(max_length=50)
	Resp_Level = models.CharField(max_length=50, choices=RESP_CHOICE) #integer or char?
	def __str__(self):
		return self.Email
	
class Merchant(models.Model):
	APPROVED = 'APP'
	REJECTED = 'RJ'
	PENDING = 'PD'
	STATUS_CHOICE = ((APPROVED, 'Approved'), (REJECTED, 'Rejected'), (PENDING, 'Pending'))
	Email = models.EmailField(max_length=50, primary_key=True)
	Password = models.CharField(max_length=50)
	FName = models.CharField(max_length=50)
	LName = models.CharField(max_length=50)
	Banking_Info = models.CharField(max_length=200) # should probably be an entity?
	Address = models.CharField(max_length=200)
	Reviewed_By = models.ForeignKey(Moderator, on_delete=models.CASCADE)
	Status = models.CharField(max_length=50, choices=STATUS_CHOICE)
	def __str__(self):
		return self.Email

class Product(models.Model):
	ID = models.AutoField(primary_key=True)
	Name = models.CharField(max_length=100)
	Description = models.TextField()
	Price = models.DecimalField(max_digits=19, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
	Brand = models.CharField(max_length=100)
	Type = models.CharField(max_length=50)
	Compatibility = models.TextField(blank=True)
	Seller_Email = models.ForeignKey(Merchant, on_delete=models.CASCADE)
	#Buyer_Email = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True) #multiple tuples of the same info except for this field Can be null?
	def __str__(self):
		return "%d %s" % (self.ID, self.Name)
	
class Order(models.Model):
	Order_Number = models.AutoField(primary_key=True)
	Total_Price = models.DecimalField(max_digits=19, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
	Shipping_Info = models.CharField(max_length=200)
	Billing_Info = models.CharField(max_length=200) # need cc info?
	Placed_By = models.ForeignKey(Customer, on_delete=models.CASCADE)
	Product_ID = models.ManyToManyField(Product)
	def __str__(self):
		return "%d %s" % (self.Order_Number, self.Placed_By)
	
class Merchant_Review(models.Model):
	Merchant_Email = models.ForeignKey(Merchant, on_delete=models.CASCADE)
	Cusomter_Email = models.ForeignKey(Customer, on_delete=models.CASCADE)
	Rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]) # rating scheme stars, numbers, etc
	Feedback = models.TextField()
	def __str__(self):
		return "%s %s" % (self.Merchant_Email, self.Cusomter_Email)
	
class Product_Review(models.Model):
	Product_ID = models.ForeignKey(Product, on_delete=models.CASCADE)
	Cusomter_Email = models.ForeignKey(Customer, on_delete=models.CASCADE)
	Rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]) # rating scheme stars, numbers, etc
	Feedback = models.TextField()
	def __str__(self):
		return "%d %s" % (self.Product_ID, self.Cusomter_Email)
	
class Cart(models.Model):
	Cusomter_Email = models.ForeignKey(Customer, on_delete=models.CASCADE)
	Product_ID = models.ManyToManyField(Product, blank=True)
	def __str__(self):
		return "%s %d" % (self.Cusomter_Email, self.Product_ID)
	
class Friends(models.Model):
	Friend_1 = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='f1')
	Friend_2 = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='f2')
	def __str__(self):
		return "%s %s" % (self.Friend_1, self.Friend_2)