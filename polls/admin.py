from django.contrib import admin
from .models import Poll, Choices, PollsUser, Vote, Follow

# Register your models here
admin.site.register(Poll)
admin.site.register(Choices)
admin.site.register(PollsUser)
admin.site.register(Vote)
admin.site.register(Follow)
