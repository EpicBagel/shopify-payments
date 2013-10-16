from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import SubscribeRedirectView, SubscribeConfirmView, ChargesView, DeleteChargeView

urlpatterns = patterns('',
	url(r'^upgrade/', TemplateView.as_view(template_name = "accounts/upgrade.html"), {}, name = 'upgrade'),
	url(r'^process-upgrade/', SubscribeRedirectView.as_view(), {}, name = 'process-upgrade'),
	url(r'^confirm-upgrade/', SubscribeConfirmView.as_view(), {}, name = 'confirm-upgrade'),
	#url(r'^process-upgrade/', SubscribeRedirectView.as_view(), {}, name = 'process-upgrade'),
	url(r'^charges/', ChargesView.as_view(), {}, name = 'charges'),
	url(r'^remove-charge/(?P<charge_id>\d+)/', DeleteChargeView.as_view(), {}, name = 'delete-charge'),
)
