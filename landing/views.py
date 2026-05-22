from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from .models import ChatHistory, DurianQuery, LeafIdentification
from .forms import RegisterForm, LoginForm, DurianQueryForm, LeafUploadForm
from .chatbot import get_chatbot_response
from .leaf_identifier import analyze_leaf_image


def landing_page(request):
    return render(request, 'landing/index.html', {'user': request.user})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'landing/register.html', {'form': form})

@login_required
def get_chat_history(request):
    """Get user's chat history"""
    from .models import ChatHistory
    chats = ChatHistory.objects.filter(user=request.user).order_by('created_at')[:50]
    chat_list = [{'question': c.question, 'answer': c.answer, 'time': c.created_at.strftime('%H:%M')} for c in chats]
    return JsonResponse({'chats': chat_list})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'landing/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('landing')


@login_required
def dashboard_view(request):
    chat_history = ChatHistory.objects.filter(user=request.user)[:10]
    leaf_ids = LeafIdentification.objects.filter(user=request.user)[:5]
    context = {
        'chat_history': chat_history,
        'leaf_identifications': leaf_ids,
        'user': request.user
    }
    return render(request, 'landing/dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    """Admin dashboard showing all registered users and their chat history"""

    # Check if user is admin
    if not request.user.is_superuser:
        messages.error(request, 'Admin access required')
        return redirect('dashboard')

    # Get all users
    all_users = User.objects.all().order_by('-date_joined')

    # Get all chat histories with user info
    all_chats = ChatHistory.objects.all().select_related('user').order_by('-created_at')[:50]

    # Get all leaf identifications
    all_leaf_ids = LeafIdentification.objects.all().select_related('user').order_by('-created_at')[:50]

    # Get statistics
    total_users = User.objects.count()
    total_chats = ChatHistory.objects.count()
    total_leaf_ids = LeafIdentification.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    # Get recent users (last 10)
    recent_users = all_users[:10]

    context = {
        'all_users': recent_users,
        'all_chats': all_chats,
        'all_leaf_ids': all_leaf_ids,
        'total_users': total_users,
        'total_chats': total_chats,
        'total_leaf_ids': total_leaf_ids,
        'active_users': active_users,
        'user': request.user,
    }
    return render(request, 'landing/admin_dashboard.html', context)
@login_required
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            response = get_chatbot_response(user_message)

            # Save to database
            ChatHistory.objects.create(
                user=request.user,
                question=user_message,
                answer=response
            )

            return JsonResponse({'response': response, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def identify_leaf_view(request):
    result = None

    if request.method == 'POST':
        form = LeafUploadForm(request.POST, request.FILES)
        if form.is_valid():
            leaf_id = form.save(commit=False)
            leaf_id.user = request.user
            leaf_id.save()

            # Analyze the image
            result = analyze_leaf_image(leaf_id.image.path)

            leaf_id.identified_variety = result.get('variety', 'Unknown')
            leaf_id.confidence_score = result.get('confidence', 0)
            leaf_id.leaf_features = result.get('features', '')
            leaf_id.save()

            messages.success(request, f'Leaf identified as {leaf_id.identified_variety}!')
    else:
        form = LeafUploadForm()

    return render(request, 'landing/leaf_upload.html', {'form': form, 'result': result})


@login_required
def submit_query(request):
    if request.method == 'POST':
        form = DurianQueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = request.user
            query.save()
            messages.success(request, 'Your question has been submitted!')
        else:
            messages.error(request, 'Please fill out the form correctly.')
    return redirect('dashboard')


@login_required
def clear_chat_history(request):
    ChatHistory.objects.filter(user=request.user).delete()
    messages.success(request, 'Chat history cleared!')
    return redirect('dashboard')