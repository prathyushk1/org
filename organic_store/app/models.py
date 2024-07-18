from django.db import models


# Create your models here.

class register(models.Model):
    reg_id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone_no=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    usertype=models.IntegerField(default=2)
    password=models.CharField(max_length=100)

    def __str__(self):

        return str(self.reg_id)

class suppliers(models.Model):
    supplier_id=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    address=models.TextField(blank=True)
    phone_no = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    id=models.ImageField(upload_to='supplier_id/',null=True,blank=True)
    usertype=models.IntegerField(default=3)
    status=models.BooleanField(default=False)


    def __str__(self):
        return str(self.supplier_id)

class delivery_agent(models.Model):
    agent_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    id_proof=models.ImageField(upload_to='agent_id/', blank=True, null=True)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    usertype=models.IntegerField(default=4)
    available=models.BooleanField(default=True)

    def __str__(self):
        return str(self.agent_id)

class product(models.Model):
    product_id=models.AutoField(primary_key=True)
    categories=models.ForeignKey('category',on_delete=models.CASCADE,to_field='category_id')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    supplier_id=models.ForeignKey('suppliers',on_delete=models.CASCADE,to_field='supplier_id')


    def __str__(self):
        return str(self.product_id)


class category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey('register',on_delete=models.CASCADE,to_field='reg_id')
    status=models.BooleanField(default=True)
    count=models.IntegerField(default=0)
    def __str__(self):
        return str(self.cart_id)

class cart_items(models.Model):
    item_id=models.AutoField(primary_key=True)
    product_id= models.ForeignKey('product',on_delete=models.CASCADE,to_field='product_id')
    qty=models.IntegerField(default=1,choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    carts_id= models.ForeignKey('cart',on_delete=models.CASCADE,to_field='cart_id')
    user_id = models.ForeignKey('register',on_delete=models.CASCADE,to_field='reg_id')
    suppliers_id = models.ForeignKey('suppliers',on_delete=models.CASCADE,to_field='supplier_id')

    def __str__(self):
        return str(self.item_id)

class orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    cart_item_id=models.ForeignKey('cart_items',on_delete=models.CASCADE,to_field='item_id')
    user_id = models.ForeignKey('register', on_delete=models.CASCADE, to_field='reg_id')
    total_product_price=models.DecimalField(max_digits=10, decimal_places=2)
    order_date=models.DateField(auto_now_add=False,blank=True,null=True)
    pickup_date=models.DateField(auto_now_add=False)
    pickup_status=models.BooleanField(default=False)
    deliver_status=models.BooleanField(default=False)
    agents_id=models.ForeignKey('delivery_agent',on_delete=models.CASCADE,to_field='agent_id')


    def __str__(self):
        return str(self.order_id)