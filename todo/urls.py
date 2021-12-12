# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("components/", views.components, name="components"),
    path("component/<int:component_id>", views.component, name="component"),
    path("observations/", views.observations, name="observations"),
    path("todos/", views.todos, name="todos"),
    path("observation/<int:observation_id>/", views.observation, name="observation"),
    path("todo/<int:todo_id>/", views.todo, name="todo"),
    path("create_observation", views.create_observation, name="create_observation"),
    path("create_todo", views.create_todo, name="create_todo"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Views
    path("get_todos", views.get_todos, name="get_todos"),
    path("edit_todo/<int:id>", views.edit_todo, name="edit_todo"),
    path("delete_todo/<int:id>", views.delete_todo, name="delete_todo"),
    path("edit_observation/<int:id>", views.edit_observation, name="edit_observation"),
    path("delete_observation/<int:id>", views.delete_observation, name="delete_observation"),
]