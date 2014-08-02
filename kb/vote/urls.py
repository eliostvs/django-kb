from django.conf.urls import patterns, url

urlpatterns = patterns(
    'kb.vote.views',

    url(r'^(?P<slug>[\w-]+)/(?P<vote>-?\d)/$', 'vote', name='vote'),
)
