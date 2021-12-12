# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

import re
from django.test import Client, TestCase

from .models import Component, Observation, Todo

# Create your tests here.

class TodoTestCase(TestCase):

    def setUp(self):
        component1 = Component.objects.create(
            type="disk"
        )
        # Component with invalid type for testing
        component2=Component.objects.create(
            type="foo"
        )

        # Create Observations
        observation1 = Observation.objects.create(
            type="NOCC-Observation", 
            component=component1, 
            status="missing_disk", 
            procedure="2145"
        )
        # Observation with invalid values for testing
        observation2 = Observation.objects.create(
            type="NOCC-Observation",
            component=component1,
            status="missing disks",
            procedure="21"
        )
        todo1 = Todo.objects.create(
            type="STS-Automation",
            comment="Reseat Disks", 
            title="reseat_disks",
            peace="False", 
            rescue="False",
            observation=observation1
        )
        # Todo with invalid fields for testing
        todo2 = Todo.objects.create(
            type="STS-Automation",
            comment="Reseat Disks", 
            title="reseat disks",
            peace="False", 
            rescue="False",
            observation=observation1
        )


    def test_is_component(self):
        """
        Test if component type is in COMPONENT_CHOICES
        """
        component = Component.objects.get(type="disk")  
        self.assertTrue(component.is_valid_component())


    def test_is_not_component(self):
        """
        Test if a component type is not in COMPONENT_CHOICES
        """
        component = Component.objects.get(type="foo")  
        self.assertFalse(component.is_valid_component())

    
    def test_is_valid_status(self):
        """
        Test observation status format, should have no spaces.
        """
        # Get observation with invalid status
        observations = Observation.objects.all()
        pattern = re.compile("[^\S+]")
        for observation in observations:
            self.assertIsNone(pattern.match(observation.status))


    def test_is_valid_title(self):
        """
        Test todo title format, should have no spaces.
        """
        # Get todo with invalid title
        todo = Todo.objects.get(title="reseat disks")
        pattern = re.compile("[^\S+]")
        self.assertIsNone(pattern.match(todo.title))

    
    def test_is_valid_procedure(self):
        """
        Test todo procedure, should be only positive ints.
        """
        observation = Observation.objects.get(procedure="2145")
        pattern = re.compile("[^0-9]")
        self.assertIsNone(pattern.match(str(observation.procedure)))
    
    
    # Client testing for 200 response from our webpages
    def test_observations_page(self):
        """
        Observations page returns 200
        """
        c = Client()
        response = c.get("/observations/")
        self.assertEqual(response.status_code, 200)

    
    def test_todos_page(self):
        """
        Todos page returns 200
        """
        c = Client()
        response = c.get("/todos/")
        self.assertEqual(response.status_code, 200)


    def test_observation_page(self):
        """
        Observations page returns 200
        """
        observation = Observation.objects.get(status="missing_disk")
        c = Client()
        response =c.get(f"/observation/{observation.id}/")
        self.assertEqual(response.status_code, 200)


    def test_todo_page(self):
        """
        Todo page returns 200
        """
        todo = Todo.objects.get(title="reseat_disks")
        c = Client()
        response =c.get(f"/todo/{todo.id}/")
        self.assertEqual(response.status_code, 200)


    def test_create_observation_page(self):
        """
        Create new observation page returns 200
        """
        c = Client()
        response =c.get("/create_observation")
        self.assertEqual(response.status_code, 200)

    
    def test_create_todo_page(self):
        """
        Create new todo page returns 200
        """
        c = Client()
        response =c.get("/create_todo")
        self.assertEqual(response.status_code, 200)

    
    def test_get_todos(self):
        """
        Test the /get_todos API, should return 200.
        """
        c = Client()
        response = c.get("/get_todos")
        self.assertEqual(response.status_code, 200)
