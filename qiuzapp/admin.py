from django.contrib import admin
from .models import User, Question

# Register your models with the Django admin site
admin.site.register(User)
admin.site.register(Question)
