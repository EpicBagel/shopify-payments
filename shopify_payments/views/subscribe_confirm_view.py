import shopify
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.contrib import messages

class SubscribeConfirmView(RedirectView):
	permanent = False
	def get_redirect_url(self, **kwargs):
		charge_id = self.request.GET.get('charge_id')
		# Get the shopify account
		shopify_user = self.request.user.social_auth.all()[0]
		shopify_session = shopify.Session(shopify_user.extra_data.get('shop'))
		shopify_session.token = shopify_user.extra_data.get('access_token')
		shopify.ShopifyResource.activate_session(shopify_session)
		# Get the charge object
		charge = shopify.RecurringApplicationCharge.find(charge_id)
		print charge.status
		if charge.status == "accepted":
			charge.activate()
			# Save the shopify charge ID
			self.request.user.charge_id = charge_id
			self.request.user.save()
			messages.success(self.request, "Thanks for upgrading to a free triel.")
		else:
			messages.success(self.request, "There was a problem confirming the charge with Shopify. Please try again.")
		return reverse('cloudfeeder:list')
