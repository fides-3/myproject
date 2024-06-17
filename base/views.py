from django.shortcuts import render , redirect
from django.views.generic import ListView , DetailView ,DeleteView,FormView

from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django .contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
# Create your views here.

def custom_logout_view(request):
   logout (request)
   return redirect('login')

def profile_view(request):
   return render(request,'profile.html')
   
class CustomLoginView(LoginView):
   template_name='login.html'
   #fields='__all_'
   #redirect_authenticated_user = True

   #def get_success_url(self):
     #return reverse_lazy('task_list')

class RegisterPage(FormView):
   template_name = 'register.html'
   form_class = UserCreationForm
   redirect_authenticated_user = True
   success_url = reverse_lazy('task_list')

   def form_valid(self,form):
      print("form is valid")
      user = form.save()
      if user is not None:
         login(self.request , user)
      return redirect(self.success_url)

   def get(self, *args,**kwargs):
      print("GET reqquest received")
      if self.request.user.is_authenticated :
         return redirect('task_list')
         return super().get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
   model = Task
   template_name='task_list.html'
   context_object_name='tasks'
#def task_list_view(request):
   # return render(request,'task')
   def get_context_data(self, **kwargs):
      context = super().get_context_data(** kwargs)
      context['tasks'] = context['tasks'].filter(user=self.request.user)
      context['count'] = context['tasks'].filter(complete=False).count()
      search_input=self.request.GET.get('search-area') or ''
      if search_input:
         context['tasks']=context['tasks'].filter(title__startswith=search_input)
         context['search_input']=search_input
      return context
      

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    template_name='task_form.html'
    success_url = reverse_lazy('task_list')


    def form_valid(self , form):
         form.instance.user = self.request.user
         return super(TaskCreate , self).form_valid(form)

     
   



class TaskDetail(DetailView):
    model = Task
    template_name='task_detail.html'
    context_object_name= 'task'

class TaskUpdate(UpdateView) :
   model = Task
   fields = ['title','description','complete']  
   success_url = reverse_lazy('task_list') 
   template_name= 'task_form.html'

   class TaskDelete(DeleteView):
      model = Task
      
      success_url = reverse_lazy('task_list')
      #context_object_name='task'
      template_name = 'task_confirm_delete.html'
      fields= '__all__'
      