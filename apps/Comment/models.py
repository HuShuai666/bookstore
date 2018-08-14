from django.db import models

# Create your models here.
from apps.art_apps.models import Arts


class Comments(models.Model):
    cid=models.AutoField(verbose_name='评论ID',primary_key=True,)
    name=models.CharField(verbose_name='评论名称',max_length=64)
    title=models.CharField(verbose_name='评论标题',max_length=64)
    content=models.CharField(verbose_name='评论内容',max_length=360)
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    arts=models.ForeignKey(Arts,models.DO_NOTHING,db_index=True,verbose_name='书籍')

    def __str__(self):
        return self.name

    class Meta:
        db_table='comment'
        verbose_name='评论信息'
        verbose_name_plural=verbose_name

