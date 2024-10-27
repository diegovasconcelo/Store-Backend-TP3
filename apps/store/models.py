from django.db import models
from django.utils.translation import gettext_lazy as _


#region: Abstract


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#region: Choices


class Gender(models.TextChoices):
    M = 'M', _('Male')
    F = 'F', _('Female')
    O = 'O', _('Other')


class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('Cash')
    CREDIT = 'credit', _('Credit Card')
    DEBIT = 'debit', _('Debit Card')
    TRANSFER = 'transfer', _('Bank Transfer')


#region: Models

class Store(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    local_number = models.CharField(
        max_length=10,
        help_text=_('Number of the place where the store is located')
    )

    def __str__(self):
        return self.name


class Client(BaseModel):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(
        max_length=1, choices=Gender.choices, blank=True, null=True
    )
    interests = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class SubCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sale(BaseModel):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    def __str__(self):
        return f'{self.client} - {self.store} - {self.total}'


class RecommendationItem(BaseModel):
    products = models.ManyToManyField('Product')
    score = models.FloatField()

    class Meta:
        ordering = ['-score']
        verbose_name = _('Recommendation Item')
        verbose_name_plural = _('Recommendation Items')

    def __str__(self):
        str_prod = ', '.join([str(product) for product in self.products.all()])
        return f'{str_prod} - {self.score}'


class Recommendation(BaseModel):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    items = models.ManyToManyField('RecommendationItem')
    confidence_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text=_('Confidence level of the recommendation')
    )
    was_purchased = models.BooleanField(
        default=False,
        help_text=_('Did the client buy the recommended products?')
    )
    reason = models.TextField(
        blank=True,
        null=True,
        help_text=_('Why did you choose that option?')
    )

    def __str__(self):
        display = f'{self.id} : {self.client} - {self.confidence_score}'
        return display
