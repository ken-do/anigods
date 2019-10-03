from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import SettingsForm
import datetime
# Create your views here.

@login_required
def settings(request):
    user = CustomUser.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            user.display_name = request.POST['display_name']
            user.name_last_updated_at = datetime.date.today()
            user.avatar = request.FILES['avatar']
            user.save()
            return redirect('users:profile')
    else:
        form = SettingsForm(None, instance=user)
    return render(request, "users/settings.html", {'form': form, 'user': user})

@login_required
def profile(request):
    return render(request, "users/profile.html", {'user': request.user})
