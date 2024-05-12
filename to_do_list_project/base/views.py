from typing import Any
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login 
from django.contrib import messages


# Create your views here.

def Login(request):
    if request.method == 'POST':
        username=request.POST['user_name']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')
    

def Register(request):
    if request.method == 'POST':
        username=request.POST['user_name']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email exist')
            else:
                user=User.objects.create_user(username=username,password=password,email=email)
                user.save()
                messages.info(request,'registered successfully')
                return redirect('login')
        else:
            messages.info(request,'password did not match')
        return redirect('register')
    else:
        return render(request,'register.html')

class TaskList(LoginRequiredMixin,ListView):
    model= Task
    template_name='task_list.html'
    context_object_name='tasks'
   
    #to access value
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()

        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)

        context['search_input'] =search_input 
        return context
    

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    template_name='task_details.html'
    context_object_name='task'
    

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    template_name='task_form.html'
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')  #after successfully adding the task it will go to the tasks homepage

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
        
            
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    template_name='task_update.html'            
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')    #after successfully updating the task it will go to the tasks homepage


class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
    template_name='task_confirm_delete.html'