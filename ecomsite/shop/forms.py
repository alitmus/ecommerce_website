from django import forms
from .models import Review,Subscriber
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['title','content','rating'
    ]
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
