from django.db import models
from apps.wine.models import WineInfo
from apps.account.models import Jh_User


class Comment(models.Model):
    '''
    消息记录表
    '''
    wine = models.ForeignKey(WineInfo)
    user = models.ForeignKey(Jh_User)
    content = models.CharField(max_length=255, verbose_name='消息内容', default='')
    type = models.IntegerField(verbose_name='状态', default=0, choices=[
        (0, '文本'), (1, '图片'), (2, '语音'), (3, '视频')])
    create_at = models.CharField(max_length=13, verbose_name='时间戳')

    class Meta:
        db_table = 'chat_comments'

    def __unicode__(self):
        return '{0}\({1}\)'.format(self.wine.code, self.user.mobile)

    def to_json(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        d['wine'] = self.wine.code
        d['user'] = self.user.mobile
        return d