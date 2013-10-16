import shopify
from django.views.generic import RedirectView
from django.conf import settings
from django.core.urlresolvers import reverse

class SubscribeRedirectView(RedirectView):
	permanent = False
	def get_redirect_url(self, **kwargs):
		# Get the shopify account
		shopify_user = self.request.user.social_auth.all()[0]
		shopify_session = shopify.Session(shopify_user.extra_data.get('shop'))
		shopify_session.token = shopify_user.extra_data.get('access_token')
		shopify.ShopifyResource.activate_session(shopify_session)
		response = shopify.RecurringApplicationCharge({
			'name' : settings.APP_NAME,
			'price' : '7.50',
			'trial_days' : 14,
			'return_url' : 'http://%s%s' % (self.request.get_host(), reverse('accounts:confirm-upgrade')),
			'test' : settings.LOCAL_DEPLOYMENT,
		})
		response.save()
		# Return the confirmation URL
		return response.to_dict()['confirmation_url']

