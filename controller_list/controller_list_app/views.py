from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .linkedlist_incompleto import *

ll = LinkedList()
controller_list = {
    'Controller List': {}
}
# Create your views here.
def index(request):
    dados = {
        'controller_list': controller_list
        }
    return render(request,'index.html', dados)

def list_control(request):
    list_to_show = {
        'list_control': controller_list
    }
    linked_list = []
    if request.method == 'POST':     
        number_to_list = request.POST.get('number_to_list')
        action_to_list = request.POST.get('select1')
        linked_list = action_list(number_to_list, action_to_list)
        list_to_show['linked_list'] = linked_list
        # list_to_show['list_control']['linked_list'] = linked_list
        
    return render(request, 'list_control.html', list_to_show)
def action_list(number_to_list, action_to_list):
    action_to_list = str(action_to_list)
    if action_to_list == '1':
        ll.insert(number_to_list)
    elif action_to_list == '2':
        ll.append(number_to_list)
    elif action_to_list == '3':
        ll.removeFirst()
    return ll.toList()

