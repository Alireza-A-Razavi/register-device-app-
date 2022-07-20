from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token

class LogoutView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseBadRequest
        else:
            logout(request)
            return redirect("/") 
            
class SignUpTempView(View):

    def post(self, request):
        if request.POST.get("username") and request.POST.get("password"):
            print(request.POST.get("username"))
            user = authenticate(
                username=request.POST.get("username"), 
                password=request.POST.get("password"),
            )
            if user:
                login(request, user)
                return redirect("/order/")
            else:
                return HttpResponseBadRequest("wrong passowrd or username, GO BACK")

        else:
            return HttpResponseBadRequest("Provide a username and password, GO BACK")

    def get(self, request):
        return render(request, "login.html", context={})
    

def get_async_csrf_token(request):
    csrftoken = get_token(request)
    return JsonResponse({'csrftoken':csrftoken})
