import shopify
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.contrib import messages
from pyactiveresource.connection import ResourceInvalid

class DeleteChargeView(RedirectView):
	permanent = False
	def get_redirect_url(self, **kwargs):
		# Get the shopify account
		shopify_user = self.request.user.social_auth.all()[0]
		shopify_session = shopify.Session(shopify_user.extra_data.get('shop'))
		shopify_session.token = shopify_user.extra_data.get('access_token')
		shopify.ShopifyResource.activate_session(shopify_session)
		# Get the charge
		charge = shopify.RecurringApplicationCharge.find(self.kwargs['charge_id'])
		print dir(charge)
		if not charge.status == "active":
			messages.error(self.request, "This charge isn't currently active, so can't yet be removed from your account.")
		else:
			try:
				charge.destroy()
				# Remove the charge from the user profile
				self.request.user.charge_id = None
				self.request.user.save()
				messages.success(self.request, "The charge has now been removed from your account")
			except ResourceInvalid, e:
				messages.error(self.request, "Charge couldn't be removed from your account. Please get in touch with us to remove.")
		# Return the confirmation URL
		return reverse("accounts:charges")

