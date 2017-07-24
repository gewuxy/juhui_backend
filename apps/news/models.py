from django.db import models

# Create your models here.
class NewsInfo(models.Model):
    '''
    资讯信息表
    '''
    title = models.CharField(max_length=100, verbose_name='标题')
    href = models.CharField(max_length=255, verbose_name='链接')
    thumb_img = models.CharField(max_length=255, verbose_name='缩略图')
    news_time = models.DateTimeField(verbose_name='新闻源时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'news_info'

    def __unicode__(self):
        return '{0} - {1}'.format(self.title, self.news_time)

    def to_json(self):
        d = {}
        d['title'] = self.title
        d['href'] = self.href
        d['thumb_img'] = self.thumb_img
        d['news_time'] = self.news_time.strftime('%Y/%m/%d %H:%M')
        return d