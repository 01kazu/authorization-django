from django.urls import path
from fifth_app.views import  register, index, user_login
app_name = "fifth_app"
urlpatterns = [
    # path("user_login", login, name="login"),
    path("register", register, name ="register"),
    path("", index, name="index"),
    path("user_login", user_login, name="user_login")
]
