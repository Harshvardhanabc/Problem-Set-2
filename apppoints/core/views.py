from rest_framework import viewsets, permissions
from .models import App, Task
from .serializers import AppSerializer, TaskSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from core.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def home(request):
    apps = App.objects.all()
    return render(request, 'user.html', {'apps': apps})

def admin_page(request):
    return render(request, 'admin.html')

def admin_dashboard(request):
    users = User.objects.all()
    assigned_apps = App.objects.select_related('uploaded_by').all()
    return render(request, 'admin.html', {
        'users': users,
        'assigned_apps': assigned_apps
    })



@login_required
def user_page(request):
    tasks = Task.objects.all()
    apps = App.objects.all()
    return render(request, 'user.html', {
        'tasks': tasks,
        'apps': apps
    })

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def points(request):
    return render(request, 'points.html')

@login_required
def points_view(request):
    return render(request, 'points.html', {'points': request.user.points})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    apps = App.objects.all()
    return render(request, 'task_list.html', {
        'tasks': tasks,
        'apps': apps
    })

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'object': task})

@login_required
def app_detail(request, pk):
    app = get_object_or_404(App, pk=pk)
    return render(request, 'app_detail.html', {'app': app})

@login_required
def upload_screenshot(request, app_id):
    if request.method == 'POST':
        screenshot = request.FILES.get('screenshot')
        app = get_object_or_404(App, id=app_id)

        if screenshot:
            app.screenshot = screenshot
            app.uploaded_by = request.user
            app.save()

            # Add points to the user
            request.user.points += app.points
            request.user.save()

            messages.success(request, f'Screenshot uploaded. {app.points} points added.')
        else:
            messages.error(request, 'Screenshot not uploaded.')

    return redirect('task-list')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


"""def add_app(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        package = request.POST.get('package')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        points = request.POST.get('points')

        App.objects.create(
            name=name,
            package=package,
            category=category,
            sub_category=sub_category,
            points=points
        )
        return redirect('/admin-page/')

    return redirect('/admin-page/')
"""

def add_app(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        package = request.POST.get('package')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        points = request.POST.get('points')
        assigned_user_id = request.POST.get('assigned_user')
        

        if all([name, package, category, sub_category, points, assigned_user_id]):
            assigned_user = User.objects.get(id=assigned_user_id)
            logo_url = request.POST.get('logo_url')

            App.objects.create(
                name=name,
                package=package,
                category=category,
                sub_category=sub_category,
                points=points,
                uploaded_by=assigned_user,
                logo_url=logo_url
            )
            return redirect('admin-page')  # Redirect after success

    # If GET or form not valid → show the form
    users = User.objects.all()
    assigned_apps = App.objects.select_related('uploaded_by').all()
    return render(request, 'admin.html', {'users': users, 'assigned_apps': assigned_apps})

    

def assigned_tasks(request):
    assigned_apps = App.objects.all()
    return render(request, 'assigned_tasks.html', {'assigned_apps': assigned_apps})


