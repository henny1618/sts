# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from django.db import models

# Create your models here.

class User(AbstractUser):
    """
    User has read and write access
    """
    pass


    def __str__(self):
        """
        Custom string function (displayed in admin interface)
        """
        return f"{self.username}"


class Component(models.Model):
    """
    Component choices for NOCC observation (Inherits from models.Model)
    Use the admin interface to add the component choices when first initializing the db
    """

    # Define component keys here
    ROUTER = 'router'
    SWITCH = 'switch'
    RACK = 'rack'
    CAMERA = 'camera'
    SERVER = 'server'
    DISK = 'disk'
    RAM = 'ram'
    INTERFACE = 'interface'
    OTHER = 'other'

    # Add tuple with keys/values
    COMPONENT_CHOICES = (
        (ROUTER, 'router'),
        (SWITCH, 'switch'),
        (RACK, 'rack'),
        (CAMERA, 'camera'),
        (SERVER, 'server'),
        (DISK, 'disk'),
        (RAM, 'ram'),
        (INTERFACE, 'interface'),
        (OTHER, 'other')
    )
    # Component type choices
    type = models.CharField(
        max_length=16,
        choices=COMPONENT_CHOICES
    )


    def __str__(self):
        """
        Custom string function (displayed in admin interface)
        Use get_FOO_display() method to get choice value (capitalized name)
        """
        return f"{self.type}"


    def is_valid_component(self):
        """
        Test for a valid component
        Returns true if type is not in component choices
        Otherwise returns false
        """
        component_list = [comp[1] for comp in self.COMPONENT_CHOICES]
        return self.type in component_list


class Observation(models.Model):
    """
    NOCC observations made remotely after receiving an alert and following
    the associated procedure.
    """

    type = models.CharField(max_length=32, default="NOCC-Automation")
    version = models.IntegerField(default=0)
    component = models.ForeignKey(
        Component,
        # Set to default 'other' when deleted
        on_delete=models.CASCADE,
        # Use to get all observations for a component
        # ex: c.compoent_observationsall()
        related_name="observations"
    )
    status = models.CharField(
        max_length=48,
        default="other",
        validators=[
            RegexValidator(
                regex='[^\S+]', 
                message="Your status should not contain spaces. Use underscores instead.",
                code="error_spaces",
                inverse_match=True
            )
        ]
    )
    procedure = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
        Custom string function (displayed in admin interface)
        """
        return f"{self.component}: {self.status}"

    
    def save(self, *args, **kwargs):
        """
        Override save method for version control
        """
        self.version = self.version + 1
        super(Observation, self).save(*args, **kwargs)



class Todo(models.Model):
    """
    STS request to troubleshoot, repair, or replace a hardware component in the datacenter.
    """

    type = models.CharField(max_length=32, default="STS-Automation")
    version = models.IntegerField(default=0)
    comment = models.CharField(max_length=32, 
        default="Investigate" 
    )
    title = models.CharField(
        max_length=32, 
        default="other_request",
        validators=[
            RegexValidator(
                regex='[^\S+]',
                message="Your status should not contain spaces. Use underscores instead.",
                code="error_spaces",
                inverse_match=True
            )
        ]
    )
    peace = models.BooleanField(
        null=True
    )
    rescue = models.BooleanField(
        null=True 
    )
    observation = models.ForeignKey(
        Observation,
        on_delete=models.CASCADE,
        related_name="todos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        """
        Custom string function (displayed in admin interface)
        """
        return f"{self.comment}"


    def save(self, *args, **kwargs):
        """
        Override save method for version control
        """
        self.version = self.version + 1
        super(Todo, self).save(*args, **kwargs)


    def human_readable_str(self):
        """
        Human readable string with STS todo instructions
        """
        return f"Todo: {self.title.lower()}\n\nObservation: {self.observation.status.lower()} {self.observation.component.type}.\n"


    def serialize(self):
        """
        Return serialized JSON
        """
        return {
            "id": self.id,
            "version": self.version,
            "type": self.type,
            "comment": self.comment,
            "title": self.title,
            "peace": self.peace,
            "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p"),
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "observation": {
                "type": self.observation.type,
                "version": self.observation.version,
                "component": self.observation.component.type,
                "status": self.observation.status,
                "procedure": self.observation.procedure,
                "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p"),
                "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            },
            "human_readable": self.human_readable_str(),
        }
