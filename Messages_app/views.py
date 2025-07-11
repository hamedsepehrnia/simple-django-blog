from django.shortcuts import render
from .forms import MessageForm
from Messages_app.models import Message


def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.save()
    else:
        form = MessageForm()
    return render(request, "Messages_app/contact.html", {'form': form})
