from django.shortcuts import render

from .forms import ContactForm, SignUpForm
# Create your views here.

def home(request):
    title = "Sign up for iPush newsletter"
    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form,
    }
	
    if form.is_valid():
        
        #form.save()
        instance = form.save(commit=False)
        signum = form.cleaned_data.get("signum")
        if not signum:
            signum = "New Jigar"
        instance.signum = signum 
#       if not instance.full_name:
#            instance.full_name = "Jigar"
#        instance.save()
        context = {
            "title": "Thank you"
        }

    return render(request, "home.html", context)
	
def feedback(request):
    title = 'Drop us a mail!'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        for key, value in form.cleaned_data.iteritems():
            print key, value
        #email = form.cleaned_data.get("email")
        #message = form.cleaned_data.get("message")
        #full_name = form.cleaned_data.get("full_name")
        #print email, message, full_name
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "forms.html", context)


