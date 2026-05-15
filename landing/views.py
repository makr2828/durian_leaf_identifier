from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Import your models and forms
from .models import ChatHistory, LeafIdentification
from .forms import LeafUploadForm

from .chatbot import get_chatbot_response  # Add this at the top

@login_required
def test_page(request):
    return render(request, 'landing/test.html')


@login_required
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            user_message = data.get('message', '')

            print(f"Chat request: {user_message}")  # Debug

            from .chatbot import get_chatbot_response
            response = get_chatbot_response(user_message)

            print(f"Chat response: {response[:100]}")  # Debug

            # Save to history
            from .models import ChatHistory
            ChatHistory.objects.create(
                user=request.user,
                question=user_message,
                answer=response
            )

            return JsonResponse({'response': response, 'success': True})

        except Exception as e:
            print(f"Chat error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def landing_page(request):
    return render(request, 'landing/index.html', {'user': request.user})


def register_view(request):
    if request.method == 'POST':
        from .forms import RegisterForm
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            return redirect('dashboard')
    else:
        from .forms import RegisterForm
        form = RegisterForm()
    return render(request, 'landing/register.html', {'form': form})


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
    # Get recent data for the user
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
    if not request.user.is_superuser:
        messages.error(request, 'Admin access required')
        return redirect('dashboard')
    return render(request, 'landing/admin_dashboard.html')


@login_required
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Simple response for testing
            response = f"🌿 Durian Expert: {user_message}\n\nI can help you identify durian varieties from their leaves! Try uploading a photo of a durian leaf."

            # Save to history (optional - only if model exists)
            try:
                ChatHistory.objects.create(
                    user=request.user,
                    question=user_message,
                    answer=response
                )
            except:
                pass

            return JsonResponse({'response': response, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .chatbot import get_chatbot_response

@login_required
@csrf_exempt
def chat_new(request):
    """New chat endpoint using updated chatbot"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            message = data.get('message', '')
            print(f"NEW CHAT - Message: {message}")
            response = get_chatbot_response(message)
            print(f"NEW CHAT - Response: {response[:100]}")
            return JsonResponse({'response': response, 'success': True})
        except Exception as e:
            print(f"NEW CHAT - Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST only'}, status=405)

@login_required
def identify_leaf_view(request):
    result = None

    if request.method == 'POST':
        form = LeafUploadForm(request.POST, request.FILES)
        if form.is_valid():
            leaf_id = form.save(commit=False)
            leaf_id.user = request.user
            leaf_id.save()

            # Show loading/processing indicator
            messages.info(request, '🤖 AI is analyzing your leaf photo... Please wait.')

            # Use REAL AI from leaf_identifier
            from .leaf_identifier import analyze_leaf_image

            # Analyze the image with AI
            result = analyze_leaf_image(leaf_id.image.path)

            if not result.get('error', False):
                # Update the record with AI results
                leaf_id.identified_variety = result['variety']
                leaf_id.confidence_score = result['confidence']
                leaf_id.leaf_features = result['features']
                leaf_id.save()

                messages.success(request,
                                 f'🌿 AI identified: {result["variety"]} with {result["confidence"]}% confidence!')
            else:
                messages.warning(request, f'AI analysis issue: {result.get("features", "Unknown error")}')
                leaf_id.delete()  # Delete the failed record
    else:
        form = LeafUploadForm()

    return render(request, 'landing/leaf_upload.html', {'form': form, 'result': result})
@login_required
def submit_query(request):
    if request.method == 'POST':
        from .forms import DurianQueryForm
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
    try:
        ChatHistory.objects.filter(user=request.user).delete()
        messages.success(request, 'Chat history cleared!')
    except:
        messages.info(request, 'No chat history to clear')
    return redirect('dashboard')


@login_required
@csrf_exempt
def chat_api(request):
    """Main chat endpoint - using working AI code"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            message = data.get('message', '')
            print(f"CHAT - Message: {message}")

            from .chatbot import get_chatbot_response
            response = get_chatbot_response(message)

            print(f"CHAT - Response: {response[:100]}")

            # Save to history
            from .models import ChatHistory
            ChatHistory.objects.create(
                user=request.user,
                question=message,
                answer=response
            )

            return JsonResponse({'response': response, 'success': True})
        except Exception as e:
            print(f"CHAT - Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST only'}, status=405)