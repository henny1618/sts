# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

import json
import re
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from .models import User, Todo, Observation, Component
from .forms import TodoForm, ObservationForm

# Create your views here.


def index(request):
    """
    Default view
    """    

    if request.method == 'GET':
        # This list can bbe null
        todo_list = Todo.objects.all()
        
        return render(request, 'todo/index.html', {
        })

def components(request):
    """
    Components view
    """

    if request.method == 'GET':
        component_list = Component.objects.all()
        return render(request, 'todo/components.html', {
            "title": "Components",
            "component_list": component_list
        })
        

def component(request, component_id):
    """
    Component view
    """
    if request.method == 'GET':
        component = get_object_or_404(Component, id=component_id)
        observation_list = Observation.objects.filter(component=component.id)
        return render(request, 'todo/component.html', {
            "title": f"Component: {component}",
            "observation_list": observation_list
        })


def observations(request):
    """
    List view for observations
    """

    if request.method == 'GET':
        # This list can be null
        observation_list = Observation.objects.all()

        return render(request, 'todo/observations.html', {
            "title": "All NOCC Observations",
            "observation_list": observation_list
        })


def observation(request, observation_id):
    """
    Observation view
    """


    if request.method == 'GET':
        observation = get_object_or_404(Observation, id=observation_id)
        return render(request, 'todo/observation.html', {
            "title": 'Observation',
            "observation": observation,
            "observation_form": ObservationForm(instance=observation)
        })


def todos(request):
    """
    Todos view
    """    

    if request.method == 'GET':
        # This list can be null
        todo_list = Todo.objects.all()
        
        return render(request, 'todo/todos.html', {
            "title": "All STS Todos",
            "todo_list": todo_list
        })


def todo(request, todo_id):
    """
    Todo view
    """

    if request.method == 'GET':
        # This list can be null
        todo = get_object_or_404(Todo, id=todo_id)

        return render(request, 'todo/todo.html', {
            "title": 'Todo',
            "todo": todo,
            "todo_form": TodoForm(instance=todo)
        })


def get_todos(request):
    """
    Get all todos
    Returns list of JSON todo objects
    """
    if request.method == 'GET':
        todos = Todo.objects.all()
        return JsonResponse([todo.serialize() for todo in todos], safe=False)



def create_todo(request):
    """
    Create a new todo
    """

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return HttpResponseRedirect(reverse("todo", args=(todo.id,)))

        # If the form is invalid return form with previous values and error message
        return render(request, "todo/create_todo.html", {
            "title": "Create a new STS Todo",
            "form": TodoForm(request.POST),
            "message": "Invalid form, please check all fields and submit again."
        })
    
    if request.method == 'GET':
        # Display error message if no observations created yet
        observations = Observation.objects.all()
        if not observations:
            return render(request, "todo/create_todo.html", {
                "message": "Create a new observation first.",
                "title": "Create a new STS Todo",
                "form": TodoForm(),
            })
        else:
            return render(request, "todo/create_todo.html", {
                "title": "Create a new STS Todo",
                "form": TodoForm(),
            })


def create_observation(request):
    """
    Create a new observation
    """

    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save()
            return HttpResponseRedirect(reverse("observation", args=(observation.id,)))

        # If the form is invalid return form with previous values and error message
        return render(request, "todo/create_observation.html", {
            "title": "Create a new NOCC observation",
            "form": ObservationForm(request.POST),
            "message": "Invalid form, please check all fields and submit again."
        })
    
    if request.method == 'GET':
        # Display error message if no components created yet
        components = Component.objects.all()
        if not components:
            return render(request, "todo/create_observation.html", {
                "message": "Add new components via the admin page.",
                "title": "Create a new NOCC observation",
                "form": ObservationForm(),
            }) 
        else:
            return render(request, "todo/create_observation.html", {
                "title": "Create a new NOCC observation",
                "form": ObservationForm(),
            }) 


@csrf_exempt
@login_required
def edit_todo(request, id):
    """
    Edit a todo using js put request
    """
    # Editing an obj must be via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get put request data
    data = json.loads(request.body)
    todo = get_object_or_404(Todo, id=id)

    title = data.get("title")
    if len(title) > 32:
        return JsonResponse({
            "error": "Your title has to be less than 32 characters."
            }, status=400)
    if ' ' in title:
        return JsonResponse({
            "error": "Your title should not contain spaces, use underscores instead."
            }, status=400)
    comment = data.get("comment")
    if len(comment) > 32:
        return JsonResponse({
            "error": "Your comment has to be less than 32 characters."
            }, status=400)
    peace = data.get("peace").capitalize()
    rescue = data.get("rescue").capitalize()
    observation_id = data.get("observation")
    observation = get_object_or_404(Observation, id=observation_id)

    todo.title = title
    todo.comment = comment
    todo.peace = peace
    todo.rescue = rescue
    todo.observation = observation

    todo.save()

    return JsonResponse({"message": "PUT saved successfully."}, status=201)


@csrf_exempt
@login_required
def edit_observation(request, id):
    """
    Edit an observation using js put request
    """
    # Editing an obj must be via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get put request data
    data = json.loads(request.body)
    observation = get_object_or_404(Observation, id=id)
    type = data.get("type")
    if len(type) > 32:
        return JsonResponse({
            "error": "Your type has to be less than 32 characters."
            }, status=400)
    component_id = data.get("component")
    component = get_object_or_404(Component, id=component_id)
    status = data.get("status")
    if len(status) > 48:
        return JsonResponse({
            "error": "Your status has to be less than 48 characters."
            }, status=400)
    if ' ' in status:
        return JsonResponse({
            "error": "Your status should not contain spaces, use underscores instead."
            }, status=400)
    procedure = data.get("procedure")
    if int(procedure) > 10000:
        return JsonResponse({
            "error": "Your status has to be less than 10000"
            }, status=400)
    if int(procedure) < 1:
        return JsonResponse({
            "error": "Your status has to be greater than 1"
            }, status=400)

    observation.type = type
    observation.component = component
    observation.status = status
    observation.procedure = procedure

    observation.save()

    return JsonResponse({"message": "PUT saved successfully."}, status=201)


@csrf_exempt
@login_required
def delete_todo(request, id):
    """
    Delete a todo using js put request
    """
    # Deleting an obj must be a via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get put request data
    data = json.loads(request.body)
    todo = get_object_or_404(Todo, id=id)

    todo.delete()

    return JsonResponse({"message": "PUT deleted successfully."}, status=201)


@csrf_exempt
@login_required
def delete_observation(request, id):
    """
    Delete an observation using js put request
    """
    # Deleting an obj must be a via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get put request data
    data = json.loads(request.body)
    observation = get_object_or_404(Observation, id=id)

    observation.delete()

    return JsonResponse({"message": "PUT deleted successfully."}, status=201)


def login_view(request):
    
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todo/login.html")


def logout_view(request):
    
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todo/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            #User = get_user_model()
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "todo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todo/register.html")