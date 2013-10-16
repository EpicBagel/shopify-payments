import shopify
from django.views.generic import TemplateView
 
class ChargesView(TemplateView):
	template_name = "accounts/charges.html"
  	def get_context_data(self, **kwargs):
 	 	context = super(ChargesView, self).get_context_data(**kwargs)
 	 	shopify_user = self.request.user.social_auth.all()[0]
 	 	shopify_session = shopify.Session(shopify_user.extra_data.get('shop'))
 	 	shopify_session.token = shopify_user.extra_data.get('access_token')
 	 	shopify.ShopifyResource.activate_session(shopify_session)
 	 	# Current charges
 	 	charges = shopify.RecurringApplicationCharge.find()
		# Add the charges to the response as a dict
  		context.update({
 	 		'charges' : [charge.to_dict() for charge in charges if charge.status == "active"],
  		})
 		return context