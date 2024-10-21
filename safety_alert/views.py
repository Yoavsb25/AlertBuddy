from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import SafetyAlert, Friendship, FriendRequest
from .forms import UserSearchForm, ProfileImageForm, CustomUserCreationForm, EmailAuthenticationForm, UserProfileEditForm


@login_required
def home(request):
    friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friends = {}

    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
        latest_alert = SafetyAlert.objects.filter(user=friend).order_by('-last_updated').first()
        friends[friend] = {
            'status': latest_alert.status if latest_alert else None,
            'last_alert_time': latest_alert.last_updated if latest_alert else None,
            'last_location': latest_alert.user_location if latest_alert else None,
            'full_name': f"{friend.first_name} {friend.last_name}"  # Include full name
        }

    return render(request, 'home.html', {'friends': friends})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.EmailBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'safety_alert/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # The form uses 'username' field for email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'safety_alert/login.html', {'form': form})


@login_required
def update_safety_status(request):
    if request.method == 'POST':
        is_safe = request.POST.get('is_safe') == 'true'
        user_location = request.POST.get('user_location')

        if user_location:
            SafetyAlert.objects.update_or_create(
                user=request.user,
                defaults={'status': is_safe, 'user_location': user_location}
            )
            return redirect('home')

    return HttpResponse('Missing required fields', status=400)


@login_required
def edit_profile(request):
    user = request.user
    user_form = UserProfileEditForm(instance=user)  # User instance
    profile_form = ProfileImageForm(instance=user.profile)  # Profile instance
    old_image = user.profile.profile_image

    if request.method == 'POST':
        user_form = UserProfileEditForm(request.POST, instance=user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=user.profile)  # Handle image uploads

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if old_image and not profile_form.cleaned_data.get('profile_image'):
                old_image.delete()  # Delete old image only if no new image is uploaded
            return redirect('profile')  # Redirect to profile page

    return render(request, 'safety_alert/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



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
    search_term = request.POST.get('username', '')
    users = User.objects.filter(username__icontains=search_term).exclude(id=request.user.id)

    friends = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friend_ids = [friend.user2.id if friend.user1 == request.user else friend.user1.id for friend in friends]

    # Get all sent friend requests by the current user that are still pending
    pending_requests = FriendRequest.objects.filter(sender=request.user, is_pending=True)
    pending_user_ids = [req.receiver.id for req in pending_requests]

    context = {
        'form': UserSearchForm(),
        'users': users,
        'friend_ids': friend_ids,
        'pending_user_ids': pending_user_ids,  # Pass pending request IDs
        'search_term': search_term
    }

    return render(request, 'search_users.html', context)



@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)

    # Check if there's already a pending or accepted friend request
    existing_request = FriendRequest.objects.filter(sender=request.user, receiver=friend, is_pending=True).first()
    existing_friendship = Friendship.objects.filter(
        Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)
    ).first()

    if existing_request:
        # Friend request already sent and is still pending
        return redirect('search_users')

    if existing_friendship:
        # Friendship already exists
        return redirect('search_users')

    # If no pending request or friendship, create a new friend request
    FriendRequest.objects.create(sender=request.user, receiver=friend)
    return redirect('search_users')


@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    friendship = get_object_or_404(Friendship,
                                   Q(user1=request.user, user2=friend) |
                                   Q(user1=friend, user2=request.user))
    friendship.delete()
    return redirect('search_users')



@login_required
def pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user, is_pending=True)
    return render(request, 'safety_alert/pending_requests.html', {'pending_requests': pending_requests})



@login_required
def approve_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.receiver == request.user:
        # Create the friendship
        Friendship.objects.create(user1=friend_request.receiver, user2=friend_request.sender)

        # Mark the friend request as processed
        friend_request.accept()

    return redirect('pending_friend_requests')


@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    # Instead of deleting, mark the request as processed
    friend_request.reject()

    return redirect('pending_friend_requests')


