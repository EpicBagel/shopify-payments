from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class PaymentBarrier(object):
	def process_request(self, request):
		upgrade_url = reverse('accounts:upgrade')
		allowed_urls = ['shopify_payments:upgrade', 'shopify_payments:process-upgrade', 'shopify_payments:confirm-upgrade']
		# If no charge ID has been set, only allow the user on t
		if request.user.is_authenticated() and not request.user.is_superuser:
			if not request.company.charge_id and not request.path in [reverse(allowed_url) for allowed_url in allowed_urls]:
				return HttpResponseRedirect(upgrade_url)