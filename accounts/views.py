from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in right after signing up
            return redirect("store:product_list")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

# Create your views here.
