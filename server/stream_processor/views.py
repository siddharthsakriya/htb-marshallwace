from django.shortcuts import render

# Create your views here.

# echo_view is a simple view that returns the same data that was sent to it.
def echo_view(request):
    """
    Echo view:
    
    This view echoes the data that was sent to it.
    """
    return request.data