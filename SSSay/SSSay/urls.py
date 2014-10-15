from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from SSSay.settings import *

admin.autodiscover()

user_patterns = patterns('User.views',
	url(r'^user/register$', 'register'),
	url(r'^user/login$', 'login'),
	url(r'^user/follow$', 'follow'),
	url(r'^user/unfollow$', 'unfollow'),
	url(r'^user/getprofile$', 'getProfile'),
	url(r'^user/getallfans$', 'getAllFans'),
	url(r'^user/getallheros$', 'getAllHeros'),
	url(r'^user/uploadportrait$','uploadPortrait'),
	url(r'^user/getfollowrelation$', 'getFollowRelation'),
	url(r'^user/getportraiturl$', 'getPortraitUrl'),
	url(r'^user/changepassword$', 'changePassword'),
	url(r'^user/logout$', 'logout'),
)

doing_patterns = patterns('Doing.views',
	url(r'^doing/getalldoing$', 'getAllDoing'),
	url(r'^doing/getdoinginfo$', 'getDoingInfo'),
	url(r'^doing/startdoing$', 'startDoing'),
	url(r'^doing/stopdoing$', 'stopDoing'),
	url(r'^doing/getpastweekrecords$', 'getPastWeekRecords'),
	url(r'^doing/getdoinghistory$', 'getDoingHistory'),
)

voice_patterns = patterns('Voice.views',
	url(r'^voice/upload_voice$', 'uploadVoice'),
	url(r'^voice/random_doing_voice$', 'randomDoingVoice'),
	url(r'^voice/random_all_voice$', 'randomAllVoice'),	
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SSSay.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
) + user_patterns + doing_patterns + voice_patterns 
