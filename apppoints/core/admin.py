from django.contrib import admin
from .models import App, Task, User

admin.site.register(User)
admin.site.register(App)
admin.site.register(Task)