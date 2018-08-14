import datetime
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from apps.Comment.models import Comments
from apps.art_apps.models import Users, Arts, Tags, Chapters, ShopCar, Orders
from apps.art_apps.utils import check_user_login


def register(request):
    if request.method == 'GET':
        return render(request, 'artsuser/register.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        member = request.POST.get('member')
        if Users.objects.filter(name=name):
            return HttpResponse('用户名已经存在')
        elif len(name) < 6 or len(name) > 20:
            return HttpResponse('用户名不规范')
        elif len(password) < 6 or len(password) > 20:
            return HttpResponse('密码不规范')
        elif Users.objects.filter(email=email):
            return HttpResponse('用户邮箱已经存在')
        else:
            icon = request.FILES.get('icon')
            icon.name = get_file_name(icon.name)
    try:
        Users.objects.get(name=name)
    except Users.DoesNotExist as e:
        Users.objects.create(name=name, password=password, email=email, icon=icon, member=member)
        return redirect('index')


def get_file_name(old_name):
    suff = '.' + old_name.split('.')[-1]
    new_name = 'IMG_{}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return new_name + suff


def login(request):
    if request.method == 'GET':
        return render(request, 'artsuser/login.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if Users.objects.filter(name=name):
            upassword = Users.objects.filter(name=name).first().password
            if upassword == password:
                request.session['name'] = name
                return redirect('index')
            else:
                return HttpResponse('密码输入错误')


def index(request):
    tid = request.GET.get('t', default=1)
    tags = Tags.objects.all()
    name = request.session.get('name')
    if name:
        img = Users.objects.filter(name=name).first().icon.url
        if tid:
            art_all = Arts.objects.all()
            arts = Arts.objects.filter(tags_id=tid).all()
            return render(request, 'artsuser/index.html',
                          {'name': name, 'tid': tid, 'tags': tags, 'art_all': art_all, 'arts': arts, 'img': img,
                           })
    else:
        art_all = Arts.objects.all()
        arts = Arts.objects.filter(tags_id=tid).all()
        return render(request, 'artsuser/index.html',
                      {'name': '请登录', 'tid': tid, 'tags': tags, 'art_all': art_all, 'arts': arts})


def loginout(request):
    request.session.clear()
    return redirect('index')


@check_user_login
def show_detail(request):
    name = request.session.get('name')
    if request.method == 'GET':
        aid = request.GET.get('aid')
        arts = Arts.objects.filter(aid=aid).all()
        chap = Chapters.objects.all().order_by('create_time')
        coms = Comments.objects.filter(arts_id=aid).all()
        return render(request, 'artsuser/content.html', {'name': name, 'arts': arts, 'chap': chap, 'coms': coms})
    elif request.method == 'POST':
        aid = request.POST.get("aid")
        newnum = request.POST.get("num")
        uid = Users.objects.filter(name=name).first().uid
        oldnum = ShopCar.objects.filter(user_id=uid).all().filter(status=1).filter(shop_id=aid).first()
        if oldnum:
            shop_car = ShopCar(
                car_id=oldnum.car_id,
                number=int(newnum) + int(oldnum.number),
                status=1,
                shop_id=aid,
                user_id=uid
            )
            shop_car.save()
            # print(aid,username,num,uid)
            return redirect('/artuser/show_detail?id=%s' % (aid))
        else:
            shop_car = ShopCar(
                number=newnum,
                status=1,
                shop_id=aid,
                user_id=uid
            )
            shop_car.save()
            # print(aid,username,num,uid)
            return redirect('/artuser/show_detail?id=%s' % (aid))


def search(request):
    if request.method == 'POST':
        key = request.POST.get('keyword')
        arts = Arts.objects.filter(Q(title__icontains=key) | Q(des__icontains=key))
        img = Arts.objects.filter(Q(title__icontains=key) | Q(des__icontains=key)).first().page_img.url
        return render(request, 'artsuser/search_handle.html', {'arts': arts, 'img': img, })


def add_car(request):
    if request.method == 'GET':
        name = request.session.get('name')
        uid = Users.objects.filter(name=name).first().uid
        shops = ShopCar.objects.filter(user_id=uid).filter(status=1).all()
        return render(request, 'car/car.html', {'name': name, 'shops': shops})


import random


def order(request):
    name = request.session.get("name")
    uid = Users.objects.filter(name=name).first().uid
    if request.method == "GET":
        shops = ShopCar.objects.filter(user_id=uid).filter(status=0).all()
        num = random.randint(1000000000, 9999999999)
        ordernum = str(num) + str(uid)
        return render(request, 'car/order.html', {"name": name, "shops": shops, "ordrenum": ordernum})
    elif request.method == "POST":
        shops_list = ShopCar.objects.filter(user_id=uid).filter(status=1).all()
        for shop in shops_list:
            number = request.POST.get("number%s" % (shop.shop_id))
            if int(number) != 0:
                shop_car = ShopCar(
                    car_id=shop.car_id,
                    number=number,
                    status=0,
                    shop_id=shop.shop_id,
                    user_id=uid,
                )
                shop_car.save()
            else:
                shop.delete()
        shops = ShopCar.objects.filter(user_id=uid).filter(status=0).all()
        num = random.randint(1000000000, 9999999999)
        ordernum = str(num) + str(uid)
        return render(request, 'car/order.html', {"name": name, "shops": shops, "ordrenum": ordernum})


def end(request):
    if request.method == "POST":
        name = request.session.get("name")
        uid = Users.objects.filter(name=name).first().uid
        order_code = request.POST.get("order_code")
        address = request.POST.get("address")
        post = request.POST.get("post")
        receiver = request.POST.get("receiver")
        mobile = request.POST.get("mobile")
        user_message = request.POST.get("user_message")
        order = Orders(
            order_code=order_code,
            address=address,
            post=post,
            receiver=receiver,
            mobile=mobile,
            user_message=user_message,
            user_id=uid,
        )
        order.save()
        oid = Orders.objects.filter(order_code=order_code).first().oid
        shops = ShopCar.objects.filter(user_id=uid).filter(status=0).all()
        for shop in shops:
            shop_car = ShopCar(
                car_id=shop.car_id,
                number=shop.number,
                status=2,
                order_id=oid,
                shop_id=shop.shop_id,
                user_id=uid,
            )
            shop_car.save()
        return redirect('check_order')


def delete(request):
    shop_id = request.GET.get("id")
    name = request.session.get("name")
    uid = Users.objects.filter(name=name).first().uid
    shop_car = ShopCar.objects.filter(user_id=uid).filter(status=1).filter(shop_id=shop_id).all()
    shop_car.delete()
    return redirect('/artuser/add_car/')


def check_order(request):
    name = request.session.get('name')
    if request.method == 'GET':
        uid = Users.objects.filter(name=name).first().uid
        shops = ShopCar.objects.filter(user_id=uid).filter(status=2).all()

        return render(request, 'car/check_order.html', {'shops': shops})


def art_add(request):
    for i in range(20):
        add = Arts(
            title='猎场' + str(i),
            des='郑秋冬',
            content='职场',
            page_img='title_img/20180727/timg.jpg',
            status=1,
            tags_id=5
        )
        add.save()
    return HttpResponse('111')



