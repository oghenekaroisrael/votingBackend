from django.contrib import admin

# Register your models here.
from .models import Vote, Election, Candidate, Poll

admin.site.register(Vote)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Poll)