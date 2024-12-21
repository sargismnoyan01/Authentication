from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from .forms import *
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from MyProject.settings import EMAIL_HOST_USER
import random
from django.contrib.auth import login,logout,authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def HomePage(request):
    return redirect('register')

class HomePageListView(ListView):
    template_name = "index.html"
    def get(self, request,id,username):
        if request.user.is_authenticated:
            users = MyUser.objects.filter(username = username,id = id)
            context = {
                'users': users,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login')
    

def UserPage(request,username):
    userr = MyUser.objects.filter(username = username)

    return render(request,'userpage.html',{'userr':userr,'this_user':username})    


def Verify_email(request,username):
    my_user = MyUser.objects.filter(username = username).first()
    email_now = my_user.email
    my_host = request.get_host()
    if request.method == 'POST':
        code_here = request.POST.get('code_here')
        if code_here == my_user.verify_code:
            return redirect(f'{my_host}/user/{my_user.username}')
    return render(request,'verify.html',{'my_user':my_user,'email_now':email_now})


def ver_code():
    return random.randint(111111,999999)

def SendCode(request, username):
    my_user = MyUser.objects.filter(username=username).first()
    email_name = my_user.email
    my_host = request.get_host()
    
    my_user.verify_code = ver_code()
    my_user.save()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }}
            .header {{
                text-align: center;
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
                color: #333333;
                line-height: 1.6;
            }}
            .footer {{
                text-align: center;
                padding: 10px;
                background: #f4f4f9;
                border-radius: 0 0 10px 10px;
                font-size: 14px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Welcome to Our Platform!</h1>
            </div>
            <div class="content">
                <p>Hello {my_user.username},</p>
                <p>This is your verification code: <a href = ""><strong>{my_user.verify_code}</strong></a></p>
                <p>If you didn’t create an account with us, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Our Platform. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    email = EmailMessage(
        subject=f'{my_host} - Verification Code',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[email_name],  
    )
    email.content_subtype = "html" 
    email.send()

    return redirect(f'/controler/{username}')



def ControlPage(request,username):
    my_user = MyUser.objects.filter(username = username).first()
    user_message = ''
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
        if str(user_message) == str(my_user.verify_code):
            my_user.is_verify = True
            my_user.save()
            return redirect(f'/{my_user.id}/{my_user.username}/')
        else:   
            return HttpResponseServerError("An error occurred while sending the verification email.")
    return render(request,'codesend.html',{'my_user':my_user})


def Register(request):
    form = CreateUserForm
    users = MyUser.objects.all()
    message = ''
    current = request.get_host()
    if request.method == 'POST':
        form = CreateUserForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            qr_image = qrcode.make(f'http://{current}/user/{obj.username}/')
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            obj.verify_code = ver_code()
            obj.qr_code.save(f'{obj.username}_qrcode.png', ContentFile(buffer.getvalue()), save=False)
            email = EmailMessage(
                subject=f"Բարի գալուստ {current} կայք",
                body=f'Հարգելի {obj.username} ձեր գրանցումը հաջողությամբ կատարվել է։\n Սա ձեր վավերացման կոդն է  {obj.verify_code}',
                from_email=EMAIL_HOST_USER,
                to = [obj.email]
            )
            email.attach(f'{obj.username}_qrcode.png', buffer.getvalue(), 'image/png')
            email.send()
            obj.save()
            message = 'success'
            return redirect(f'login')
        else:
            message = form.errors

    return render(request,'register.html',{'form':form,'message':message,'users':users,'current':current})





@csrf_exempt
def save_qr_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            qr_data = qr_data.replace('[','')
            qr_data = qr_data.replace(']','')
            qr_data = qr_data.split(',')
            username = qr_data[0]
            userr = MyUser.objects.get(username = username)
            verify_codee = qr_data[1]
            userrname = qr_data[0]
            print(userrname == userr.username)
            print(str(userr.verify_code) == verify_codee)
            user = authenticate(username=username,verify_code = verify_codee)
            if user:
                login(request,user)
                return redirect(f'/{userr.id}/{userr.username}/')
            else:
                return redirect('register')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request,'qr_scanner.html')


def send_qr_email(request,my_email):
    host_name = request.get_host
    code = random.randint(100000000,999999999)
    user = MyUser.objects.get(email = my_email)
    user.verify_code = code
    user.save()
    qr_image = qrcode.make(f'[{user.username},{user.verify_code}]')
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    user.qr_code.save(f'{user.username}_qrcode.png', ContentFile(buffer.getvalue()), save=False)
    email = EmailMessage(
        subject=host_name,
        body='Սկանավորեք ձեր QR կոդը',
        from_email=EMAIL_HOST_USER,
        to=[my_email]
    )
    email.attach(f'{user.username}_qrcode.png', buffer.getvalue(), 'image/png')
    email.send()
    return redirect('save_qr_data')
    

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect(f'/{user.id}/{user.username}/')
        else:
            return redirect('register')
    return render(request,'login.html')


def WriteEmail(request):
    email = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        return redirect(f'/for_user_login/{email}/')
    return render(request,'qr_email.html',{'email':email})




def Logout(request):
    logout(request)
    return redirect('register')























































