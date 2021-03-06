from django.shortcuts import render, get_object_or_404
from .models import Module

# Create your views here.

def index(request):
    modules = Module.objects.all()
    return render(request, 'modules/index.html', {"modules" : modules})

#def detail(request, module_id):
#    module = get_object_or_404(Module, pk=module_id)
#    return render(request, 'grbs/individual_page.html', {'module': module})
