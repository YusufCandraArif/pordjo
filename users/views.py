from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# def updateCustomer(request, pk):
# 	order = Customer.objects.get(id=pk)
# 	form = CustomerForm(instance=order)

# 	if request.method == 'POST':
# 		form = CustomerForm(request.POST, instance=order)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'accounts/customer_update.html', context)



@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    uform = UserUpdateForm(instance=profile)
    pform = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('profile')

    return render(request, 'users/profile.html', {'uform': uform, 'pform': pform})


# @login_required
# def profile(request):
#     profile = Profile.objects.get_or_create(user=request.user)
#     order = Customer.objects.get(id=pk)
#     if request.method == 'POST':
#         uform = UserUpdateForm(request.POST, instance=request.user)
#         pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

#         if uform.is_valid() and pform.is_valid():
#             uform.save()
#             pform.save()
#             messages.success(request, f'Account has been updated.')
#             return redirect('profile')
#     else:
#         uform = UserUpdateForm(instance=profile)
#         pform = ProfileUpdateForm(instance=profile)

#     return render(request, 'users/profile.html', {'uform': uform, 'pform': pform})



@login_required
def SearchView(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = User.objects.filter(username__contains=kerko)
        context = {
            'results':results
        }
        return render(request, 'users/search_result.html', context)
