from django.shortcuts import render

from .forms import SignUpForm
# Create your views here.

def home(request):
    title = "Welcome " 
#    if request.user.is_authenticated():
#        title = "My Title %s" %(request.user)
    # Add a form here
    form = SignUpForm(request.POST or None)
    if form.is_valid():
         instance = form.save(commit=False)
    context = {
        "title": title,
        "form": form,
    }
    return render(request, "home.html", context)
	
