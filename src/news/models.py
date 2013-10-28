# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _


from .. accounts.models import User


class News(models.Model):
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'), help_text=_('Use Markdown and HTML'))
    created = models.DateTimeField(_(u'created'), auto_now_add=True)
    author = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ['-created']
        verbose_name = _(u'News')
        verbose_name_plural = _(u'News')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news:news', [self.pk], {})

    def search(self):
        return dict(source=_(u'News'), title=self.title, desc=self.content)

    def get_next(self):
        try:
            return News.objects.all().filter(created__gt=self.created).exclude(pk=self.pk).order_by('created')[:1].get()
        except News.DoesNotExist:
            return

    def get_prev(self):
        try:
            return News.objects.all().filter(created__lt=self.created).exclude(pk=self.pk).order_by('-created')[:1].get()
        except News.DoesNotExist:
            return


class NewsForm(forms.ModelForm):
    class Meta:
        model = News        