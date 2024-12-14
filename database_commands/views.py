from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate
# Create your views here.

def login_flutter(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            
            login(request, user)

            response = JsonResponse({'Cookie': request.session.session_key})

            # Optionally, you can set a session cookie or a custom token
            # If you're using sessions (default in Django), the sessionid cookie is automatically set
            # For example, if you want to manually set a cookie, you could do:
            # response.set_cookie('sessionid', request.session.session_key)

            # Or, if you're using JWT tokens:
            # token = generate_jwt_token(user)  # Implement JWT token generation if needed
            # response.set_cookie('token', token)

            return response
        else:

            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    
def logout_flutter(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
