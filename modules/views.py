from django.shortcuts import render, get_object_or_404
from .models import Module

# Create your views here.
MODULES_TO_DISPLAY = [""]

def index(request):
    modules = Module.objects.order_by('name')
    all_keywords = []
    for module in modules:
        if module.primary_keywords is not None:
            for keyword in module.primary_keywords:
                all_keywords.append(keyword)
    all_keywords = set(all_keywords)
    
    return render(request, 'modules/index.html', {"modules" : modules, "all_keywords" : all_keywords})

#def detail(request, module_id):
#    module = get_object_or_404(Module, pk=module_id)
#    return render(request, 'grbs/individual_page.html', {'module': module})
