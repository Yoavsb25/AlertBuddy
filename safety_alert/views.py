from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, User
from django.contrib.auth import login, authenticate
from django.db.models import Q
from .models import SafetyAlert, Friendship, FriendRequest
from .forms import SafetyAlertForm, UserSearchForm, ProfileImageForm


@login_required
def home(request):
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friends = {}


    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
        latest_alert = SafetyAlert.objects.filter(user=friend).order_by('-last_updated').first()
        friends[friend] = {
            'status': latest_alert.status if latest_alert else None,
            'last_alert_time': latest_alert.last_updated if latest_alert else None
        }

    return render(request, 'home.html', {'friends': friends})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'safety_alert/login.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'safety_alert/login.html', {'form': form})


@login_required
def update_safety_status(request):
    if request.method == 'POST':
        # Fix: Retrieve the correct 'is_safe' from the form
        is_safe = request.POST.get('is_safe')
        user_location = request.POST.get('user_location')

        if is_safe is None or user_location is None:
            return HttpResponse('Missing required fields', status=400)

        # Convert the string 'true'/'false' to a boolean
        is_safe = is_safe.lower() == 'true'

        # Update or create the SafetyAlert instance for the user
        safety_alert, created = SafetyAlert.objects.update_or_create(
            user=request.user,
            defaults={'status': is_safe, 'user_location': user_location}
        )

        return redirect('home')

    return HttpResponse(status=405)  # Method not allowed if not POST


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')


@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.profile_image = form.cleaned_data['profile_image']
            profile.save()
            return redirect('profile')
    else:
        form = ProfileImageForm()
    return render(request, 'upload_profile_image.html', {'form': form})


def search_users(request):
    search_term = request.POST.get('username', '') if request.method == 'POST' else ''
    users = User.objects.filter(username__icontains=search_term).exclude(id=request.user.id)

    friends = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friend_ids = [friend.user2.id if friend.user1 == request.user else friend.user1.id for friend in friends]

    return render(request, 'search_users.html', {
        'form': UserSearchForm(),
        'users': users,
        'friend_ids': friend_ids,
    })


@login_required
def add_friend(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=user_id)
        FriendRequest.objects.create(sender=request.user, receiver=friend)
        return redirect('search_users')


@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    friendship = Friendship.objects.filter(
        Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)).first()

    if friendship:
        friendship.delete()

    return redirect('search_users')


@login_required
def pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'safety_alert/pending_requests.html', {'pending_requests': pending_requests})


@login_required
def approve_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.receiver == request.user:
        Friendship.objects.create(user1=friend_request.receiver, user2=friend_request.sender)
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        friend_request.delete()

    return redirect('pending_friend_requests')


@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    friend_request.delete()
    return redirect('pending_friend_requests')

