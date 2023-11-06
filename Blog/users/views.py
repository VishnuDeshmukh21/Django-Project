from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,CustomAuthenticationForm
from firebase_admin import auth
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import login_required
from pymongo import MongoClient
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Profile
from pymongo import MongoClient
from django.http import JsonResponse
from .serializers import UserProfileSerializer
from firebase_admin import auth


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            # Check if the user already exists
            User = get_user_model()
            if User.objects.filter(username=email.split('@')[0]).exists():
                messages.error(request, 'A user with that email already exists.')
                return redirect('register')
            else:
                try:
                    #Create a Firebase user
                    firebase_user = auth.create_user(email=email, password=password)
                    firebase_uid = firebase_user.uid

                    # Create a Django user
                    User = get_user_model()
                    django_user = User.objects.create_user(username=email.split('@')[0], email=email, password=password)
                    django_user.first_name = first_name
                    django_user.last_name = last_name
                    django_user.save()

                    # Create a Profile object and associate it with the Django user and Firebase UID
                    profile,created = Profile.objects.get_or_create(user=django_user)
                    profile.uid=firebase_uid
                    if created:
                        profile.save()

                    form.cleaned_data['username'] = email.split('@')[0]
                    user_name = form.cleaned_data.get('username')

                    data=f'username: {user_name}, email: {email}'
                    response_data={'username':user_name, 'email':email}

                    client = MongoClient('mongodb://localhost:27017/')
                    # Access the  database
                    db = client['django']
                    # Access the 'users' collection within the 'django' database
                    collection = db['users']
                    # Insert the JSON data into the 'static' collection
                    collection.insert_one(response_data)
                    # Close the MongoDB client connection
                    client.close()

                    messages.success(request, 'Account created successfully. You can now log in.')
                    messages.info(request, data)

                    return redirect('login')

                except Exception as e:
                    messages.error(request, f'Error creating user: {str(e)}')
                    return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



class UserLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    def form_valid(self, authentication_form):
        response = super(UserLoginView, self).form_valid(authentication_form)

        if self.request.user.is_authenticated:
            # FirebaseUidMiddleware will handle Firebase UID validation
            pass
        user = self.request.user
        serializer = UserProfileSerializer(user)
        messages.success(self.request,serializer.data)
        return response
        
    def form_invalid(self, authentication_form):
        return super(UserLoginView, self).form_invalid(authentication_form)

@login_required
def view_profile(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserProfileSerializer(user)
        return render(request,'users/profile.html',{'response_data':serializer.data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=401)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            new_username = u_form.cleaned_data.get('username')

            # Check if the new username already exists in the database
            User = get_user_model()

            if User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
                messages.error(request, 'Username already taken. Please choose a different one.')
            else:
                u_form.save()
                p_form.save()
                user = request.user
                serializer = UserProfileSerializer(user)
                messages.success(request, serializer.data)
                return redirect('profile_view')            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/editprofile.html', context)
