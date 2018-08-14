import xadmin
# from .models import Users, Tags, Arts, Chapters
from apps.art_apps import models
from xadmin import views


class BaseSetting(object):
    # 主题修改
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 整体配置
    site_title = '小说电商平台后台管理系统'
    site_footer = '千锋上海python-1802'
    menu_style = 'accordion'  # 菜单折叠
    global_search_models = [models.Users, models.Tags, models.Arts,
                            models.Chapters]
    global_models_icon = {
        models.Arts: "glyphicon glyphicon-book",
        models.Tags: "fa fa-cloud",
        models.Chapters: "glyphicon glyphicon-th-list",
        models.Users: "glyphicon glyphicon-user",
        # Comment: "glyphicon glyphicon-list-alt",
        # UserMessage:  "glyphicon glyphicon-list-alt",
    }  # 设置models的全局图标


'''
标签自定义展示对象
'''
class TagAdmin(object):
    list_display = ['tag', 'tag_des', 'create_time', 'status']
    search_fields = ['tag', 'tag_des', 'create_time']
    list_filter = ['tag', 'tag_des', 'status']
    list_editable = ['tag', 'tag_des']
#
#
#
class ArtAdmin(object):
    list_display = ['title', 'des', 'content', 'page_img' ,'create_time', 'tags']
    search_fields = ['title', 'des', 'content', 'page_img', 'create_time']
    list_filter = ['title', 'des', 'create_time', 'status']
    show_detail_fields = ['title']
    list_per_page = 5
    list_editable = ['title', 'des' ,'content']
    style_fields = {'content': 'ueditor'}

#
class ChapterAdmin(object):
    list_display = ['arts', 'title', 'cha_content', 'create_time']
    search_fields = ['arts', 'title', 'cha_content', 'create_time']
    list_filter = ['arts', 'title', 'cha_content', 'create_time']
    list_per_page = 5
#
# class CommentAdmin(object):
#     list_display = ['name', 'title', 'text', 'created_time', 'art', 'flag']
#     search_fields =  ['name', 'title', 'text', 'created_time', 'art']
#     list_per_page = 5


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(models.Users)
xadmin.site.register(models.Tags, TagAdmin)
xadmin.site.register(models.Arts, ArtAdmin)
xadmin.site.register(models.Chapters, ChapterAdmin)
# xadmin.site.register(Comment, CommentAdmin)
