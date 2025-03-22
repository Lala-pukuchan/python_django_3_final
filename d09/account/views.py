# Create your views here.
# account/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def account_view(request):
    """
    GET時: ユーザーがログイン済みかどうかで表示を切り替えるためのページを返す。
    JavaScriptで、このページ内部にあるフォームか、あるいは状態表示を切り替える仕組みにする。
    """
    context = {}
    if request.user.is_authenticated:
        context['is_authenticated'] = True
        context['username'] = request.user.username
    else:
        context['is_authenticated'] = False
        # Django標準の認証フォーム(ユーザー名/パスワード入力)
        form = AuthenticationForm()
        context['form'] = form
    return render(request, 'account/account.html', context)

def login_ajax(request):
    """
    AJAXで受け取るログイン処理:
    - 成功したら { 'success': True } を返却
    - 失敗したら { 'success': False, 'errors': [...] } を返却
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                # start user session
                # make user login
                # save user info to session
                login(request, user)
                return JsonResponse({'success': True})
        # バリデーションエラーの場合
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def logout_ajax(request):
    """
    AJAXで受け取るログアウト処理
    """
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})
