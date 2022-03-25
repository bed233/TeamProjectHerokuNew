from django.db import models

# model defines menuItems that contain fields highlighted below e.g allergies and calories
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')  # Creates a many-to-many relationship between
    # Menuitem and category
    allergy = models.ManyToManyField('Allergy', related_name='item')
    calories = models.CharField(max_length=10, blank=True, null=True)

    def get_allergy_values(self):
        ret = ''
        print(self.allergy.all())
        # use models.ManyToMany field's all() method to return all the Department objects that this employee belongs to.
        for allergy in self.allergy.all():
            ret = ret + allergy.name + ', '
        # remove the last ',' and return the value.
        return ret[:-2]

    def __str__(self):  # Formats the objects
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='allergy_images/')

    def __str__(self):
        return self.name

# an order object that holds all menu items being ordered
class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)
    order_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    ready_to_deliver = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    need_help = models.BooleanField(default=False)
    table_number = models.IntegerField(default=0)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'  # Returns a string representing date and time.

class ItemQuantity(models.Model):
    item = models.ManyToManyField('MenuItem', related_name='ItemOrder', blank=True)
    orderID = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.item
