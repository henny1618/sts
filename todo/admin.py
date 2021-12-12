# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Component, Observation, Todo


class ComponentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']


class ObservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'component', 'procedure']


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'title', 'observation']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(Todo, TodoAdmin)