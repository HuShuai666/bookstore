from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class Users(models.Model):
    STATUS_CHOICES = (
        (1, '普通会员'),
        (2, 'VIP会员'),
        (3, '黄金会员')
    )
    uid = models.AutoField('用户ID', primary_key=True)
    name = models.CharField('用户名', max_length=64)
    password = models.CharField(verbose_name=u'密码', max_length=64)
    icon = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='media/%Y%m%d')
    email = models.CharField(verbose_name=u'邮箱', max_length=64)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    member = models.IntegerField(verbose_name='会员等级', default=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


class Tags(models.Model):
    STATUS_CHOICES = (
        (1, '未删除'),
        (2, '已删除')
    )
    tid = models.AutoField('标签ID', primary_key=True)
    tag = models.CharField('标签', max_length=64)
    tag_des = models.CharField('标签描述', max_length=1000)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, max_length=1)
    status = models.IntegerField(verbose_name='控制字段', choices=STATUS_CHOICES)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'tags'
        verbose_name = '书籍标签'
        verbose_name_plural = verbose_name


class Arts(models.Model):
    STATUS_CHOICES = (
        (1, '未删除'),
        (2, '已删除')
    )
    aid = models.AutoField('书籍ID', primary_key=True)
    title = models.CharField('书籍标题', max_length=64)
    des = models.CharField(verbose_name=u'作者', max_length=1000)
    content = models.CharField(verbose_name='内容', max_length=1000)
    page_img = models.ImageField(verbose_name='封面', max_length=100, upload_to='title_img/%Y%m%d')
    price = models.DecimalField(verbose_name="单价", max_digits=7, decimal_places=2, default=100.00)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.IntegerField('控制字段', choices=STATUS_CHOICES)
    tags = models.ForeignKey(Tags, models.DO_NOTHING, db_column='tags_id', db_index=True, verbose_name='书籍标签')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'arts'
        verbose_name = '书籍信息'
        verbose_name_plural = verbose_name


class Chapters(models.Model):
    cid = models.AutoField('章节ID', primary_key=True)
    arts = models.ForeignKey(Arts, models.DO_NOTHING, db_column='arts_id', db_index=True, verbose_name='书籍')
    title = models.CharField(verbose_name='标题', max_length=64)
    cha_content = models.CharField(verbose_name='章节内容', max_length=1000)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, max_length=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'chapter'
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class Orders(models.Model):
    ORDER_STATUS = (
        (1, '正常'),
        (0, '异常'),
        (-1, '删除'),
    )

    oid = models.AutoField('订单ID', primary_key=True)
    order_code = models.CharField('订单号', max_length=255)
    address = models.CharField('配送地址', max_length=255)
    post = models.CharField('邮编', max_length=255)
    receiver = models.CharField('收货人', max_length=255)
    mobile = models.CharField('手机号', max_length=11)
    user_message = models.CharField('附加信息', max_length=255)
    create_date = models.DateTimeField('创建日期', max_length=0, auto_created=True, auto_now=True)
    pay_date = models.DateTimeField('支付时间', max_length=0,
                                    blank=True, null=True)
    delivery_date = models.DateTimeField('交易日期', blank=True, null=True)
    confirm_date = models.DateTimeField('确认日期', blank=True, null=True)
    """ 1正常 0 异常, -1 删除 """
    status = models.IntegerField('订单状态', choices=ORDER_STATUS, default=1)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', verbose_name="用户ID")

    def __str__(self):
        return self.order_code

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单管理'


class ShopCar(models.Model):
    STATUS_CHOICES = (
        (1, '未删除'),
        (2, '已删除'),
        (0, '禁止')
    )
    car_id = models.AutoField(verbose_name="ID", primary_key=True)
    number = models.IntegerField(verbose_name="商品数量", default=0)
    shop = models.ForeignKey(Arts, models.DO_NOTHING, verbose_name="书籍ID")
    user = models.ForeignKey("Users", models.DO_NOTHING, db_column="uid", verbose_name="用户ID")
    order = models.ForeignKey("Orders", on_delete=models.SET_NULL, db_column="oid", null=True, verbose_name="订单ID")
    status = models.IntegerField(verbose_name="购物状态", choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.shop.title

    class Meta:
        db_table = "shop_car"
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class Content(models.Model):
    content = HTMLField()
