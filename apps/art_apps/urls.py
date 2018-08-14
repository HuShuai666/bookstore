from django.conf.urls import url



# http://127.0.0.1:8000/media + user/homebg.png
# 二进制数据
from apps.art_apps import views

urlpatterns = [

url('register/',views.register,name='register'),
    url('login/',views.login,name='login'),
    url('index/',views.index,name='index'),
    url('loginout/',views.loginout,name='loginout'),
    url('show_detail/',views.show_detail,name='show_detail'),
    url('art_add/',views.art_add,),
    url('search/',views.search,name='search'),
    url('add_car/',views.add_car,name='add_car'),
    url('order/',views.order,name='order'),
    url('end/',views.end,name='end'),
    url('delete/',views.delete,name='delete'),
    url('check_order',views.check_order,name='check_order'),

]
