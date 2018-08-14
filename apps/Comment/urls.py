from django.conf.urls import url



# http://127.0.0.1:8000/media + user/homebg.png
# 二进制数据
from apps.Comment import views

urlpatterns = [
url('art/',views.art,name='art'),





]
