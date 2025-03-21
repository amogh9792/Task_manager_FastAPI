import requests
from django.shortcuts import render, redirect

FASTAPI_URL = 'http://127.0.0.1:8001'  # Your FastAPI URL

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        response = requests.post(f'{FASTAPI_URL}/login/', json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            request.session['jwt_token'] = token
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    
    # GET request renders the login page
    return render(request, 'login.html')



def dashboard(request):
    token = request.session.get('jwt_token')
    if not token:
        return redirect('login')
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{FASTAPI_URL}/tasks/', headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()
    else:
        tasks = []
    
    return render(request, 'dashboard.html', {'tasks': tasks})
