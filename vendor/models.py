from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Q


class Vendor(models.Model):
    
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z][A-Za-z\s&.'-]*$",
                message="Name must use letters and spaces only (no numbers).",
            )
        ],
    )
    delivery_rating = models.FloatField(
        default=0,
        help_text="1-5 scale",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    delivery_rating = models.FloatField(
    default=1,
    help_text="1-5 scale",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)

    quality_rating = models.FloatField(
    default=1,
    help_text="1-5 scale",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)

    price_rating = models.FloatField(
    default=1,
    help_text="1-5 scale",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)

    communication_rating = models.FloatField(
    default=1,
    help_text="1-5 scale",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(delivery_rating__gte=1, delivery_rating__lte=5),
                name="vendor_delivery_rating_range",
            ),
            models.CheckConstraint(
                condition=Q(quality_rating__gte=1, quality_rating__lte=5),
                name="vendor_quality_rating_range",
            ),
            models.CheckConstraint(
                condition=Q(price_rating__gte=1, price_rating__lte=5),
                name="vendor_price_rating_range",
            ),
            models.CheckConstraint(
                condition=Q(communication_rating__gte=1, communication_rating__lte=5),
                name="vendor_communication_rating_range",
            ),
        ]


    def __str__(self):
        return self.name

    def vendor_score(self):
        
        return round(
            (self.delivery_rating +
             self.quality_rating +
             self.price_rating +
             self.communication_rating) / 4,2
        )
