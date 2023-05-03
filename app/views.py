from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import User, App, App2
from django.contrib.sessions.models import Session
from django.utils import timezone
import hashlib
from django.contrib.auth.hashers import make_password
import bcrypt

def index(request):
    # 현재 세션 ID를 가져옵니다.
    session_key = request.session.session_key
    if not session_key:
        # 세션 ID가 없으면, 새로운 세션을 생성합니다.
        request.session.cycle_key()
        session_key = request.session.session_key

    # 현재 세션에 대한 방문자 정보를 가져옵니다.
    session = Session.objects.filter(session_key=session_key).first()
    if session:
        # 이미 방문한 경우, 방문자 수를 증가시키지 않습니다.
        session.expire_date = timezone.now() + timezone.timedelta(days=1)
        session.save()
    else:
        # 처음 방문한 경우, 방문자 수를 증가시킵니다.
        Session.objects.create(session_key=session_key, expire_date=timezone.now() + timezone.timedelta(days=1))
    
    # 전체 방문자 수를 가져옵니다.
    total_visitors = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # index.html 템플릿을 렌더링합니다.
    return render(request, 'index.html', {'total_visitors': total_visitors})


def noodle_worldcup(request):
    return render(request, 'noodle_worldcup.html')

def chicken_worldcup(request):
    return render(request, 'chicken_worldcup.html')

def snack_worldcup(request):
    return render(request, 'snack_worldcup.html')

def food_worldcup(request):
    return render(request, 'food_worldcup.html')

def signup(request):
  if request.method == 'POST':
    # Save member information
    email = request.POST.get('email')
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')
    hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # generate encrypted password
    user = User(email=email, name=name, pwd=hashed_pwd)
    user.save()
    return render(request, 'signup_success.html')

  return render(request, 'signup.html')

def signin(request):
  if request.method == 'POST':
    # 회원정보 조회
    email = request.POST.get('email')
    pwd = request.POST.get('pwd')

    try:
      # select * from user where email=? and pwd=?
      user = User.objects.get(email=email)
      hashed_pwd = user.pwd

      if bcrypt.checkpw(pwd.encode('utf-8'), hashed_pwd.encode('utf-8')):
        request.session['email'] = email
        return render(request, 'signin_success.html')
      else:
        return render(request, 'signin_fail.html') 
    except Exception as e:
      return render(request, 'signin_fail.html')

  return render(request, 'signin.html')

def signout(request):
  del request.session['email']  # 개별 삭제
  request.session.flush()  # 전체 삭제

  return HttpResponseRedirect('/index/')

def email_check(request):
    email = request.GET.get('email')
    try:
        User.objects.get(email=email)
        result = True
    except User.DoesNotExist:
        result = False
    return JsonResponse({'result': result})

def write(request):
  if request.method == 'POST':
    category = request.POST.get('category')
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    if 'email' in request.session:
      try:
        email = request.session['email']
        # select * from user where email = ?
        user = User.objects.get(email=email)
        # insert into app (title, content, user_id) values (?, ?, ?)
        app = App(category=category, title=title, content=content, user=user)
        app.save()
        return render(request, 'write_success.html')
      except User.DoesNotExist:
        pass
    return render(request, 'write_fail.html')

  return render(request, 'write.html')

def list(request):
  page = request.GET.get('page')
  if not page:
    page = '1'
  page = int(page)
# GET를 POST로 바꾸면 POST방식 POST는 ?없음 
  prd = request.GET.get('prd')
# 공백 if prd == False: prd = ''도 가능 혹은 위의 식에 공백 추가 prd = request.GET.get('prd', '') 도 가능
  if not prd:
    prd = ''
  
  app_list = App.objects.order_by('-id')
  p = Paginator(app_list, 10)
  page_obj = p.page(page)
  s_page = (page - 1 ) // 10 * 10 + 1
  e_page = s_page + 9
  pages = range(s_page, e_page + 1)
  context = {
        'app_list': page_obj.object_list,
        'data': page_obj,
        'page': page,
        'pages': p.get_elided_page_range(number=page),
  }
  return render(request, 'list.html', context)

from django.contrib.auth.decorators import login_required

def detail(request, id):
  # select * from app where id = ?
  app = App.objects.get(id=id)
  context = { 
    'app' : app 
  }
  return render(request, 'detail.html', context)


def update(request, id):
    app = App.objects.get(id=id)

    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if 'email' in request.session:
            try:
                email = request.session['email']
                user = User.objects.get(email=email)
                app.category = category
                app.title = title
                app.content = content
                app.user = user
                app.save()
                return render(request, 'update_success.html')
            except User.DoesNotExist:
                pass
        # 로그인이 되어있지 않는 경우, 수정 불가
        return render(request, 'write_fail.html')

    context = { 
        'app' : app 
    }
   
    return render(request, 'update.html', context)



def notice(request):
  page = request.GET.get('page')
  if not page:
    page = '1'
  page = int(page)
# GET를 POST로 바꾸면 POST방식 POST는 ?없음 
  prd = request.GET.get('prd')
# 공백 if prd == False: prd = ''도 가능 혹은 위의 식에 공백 추가 prd = request.GET.get('prd', '') 도 가능
  if not prd:
    prd = ''
  
  app_notice = App2.objects.order_by('-id')
  p = Paginator(app_notice, 10)
  page_obj = p.page(page)
  s_page = (page - 1 ) // 10 * 10 + 1
  e_page = s_page + 9
  pages = range(s_page, e_page + 1)
  context = {
        'app_notice': page_obj.object_list,
        'data': page_obj,
        'page': page,
        'pages': p.get_elided_page_range(number=page),
  }
  return render(request, 'notice.html', context)


def write2(request):
  if request.method == 'POST':
    category2 = request.POST.get('category2')
    title2 = request.POST.get('title2')
    content2 = request.POST.get('content2')
    
    if 'email' in request.session:
      try:
        email = request.session['email']
        # select * from user where email = ?
        user = User.objects.get(email=email)
        # insert into app (title, content, user_id) values (?, ?, ?)
        app2 = App2(category=category2, title=title2, content=content2, user=user)
        app2.save()
        return render(request, 'write_success2.html')
      except User.DoesNotExist:
        pass
    return render(request, 'write_fail.html')

  return render(request, 'write2.html')


def detail2(request, id):
  # select * from app where id = ?
  app2 = App2.objects.get(id=id)
  context = { 
    'app2' : app2 
  }
  return render(request, 'detail2.html', context)

def update2(request, id):
  # select * from app where id = ?
  app2 = App2.objects.get(id=id)

  if request.method == 'POST':
    category2 = request.POST.get('category2')
    title2 = request.POST.get('title2')
    content2 = request.POST.get('content2')
    if 'email' in request.session:
      try:
          email = request.session['email']
          user = User.objects.get(email=email)
          app2.category = category2
          app2.title = title2
          app2.content = content2
          app2.save()
          return render(request, 'update_success2.html')
      except User.DoesNotExist:
          pass
      # 로그인이 되어있지 않는 경우, 수정 불가
    return render(request, 'write_fail.html')

  context = { 
    'app2' : app2 
  }
  return render(request, 'update2.html', context)
