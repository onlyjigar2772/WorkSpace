from django.shortcuts import render


def about(request):
    return render(request, "about.html", {})

def search(request):
    return render(request, "search.html", {})
	
def statistics(request):
    return render(request, "statistics.html", {})
	
def commits(request):
    return render(request, "commits.html", {})
	
