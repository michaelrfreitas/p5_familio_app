import stripe
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from member.models import CustomUser
from django.contrib import messages
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


@login_required(redirect_field_name='account_login')
def plans(request):
    """ A view to return the plans page """
    return render(request, 'subscriber/plans.html')


@login_required(redirect_field_name='account_login')
def subscribed(request, user_id):
    """ Member approves and desapproves to Familio member. """
    subscribe = get_object_or_404(CustomUser, id=user_id)
    subscribe.subscription = not subscribe.subscription
    subscribe.save()
    messages.success(
        request, f'You changed your plan successfully!')  # noqa
    return redirect('plans')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        if os.environ.get('DEVELOPMENT'):
            domain_url = os.getenv('DOMAIN_URL')
        else:
            domain_url = f"{ request.scheme }://{request.META['HTTP_HOST'] }/"
        print(domain_url)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,  # noqa
                success_url=f'{domain_url}subscriber/subscribed/{request.user.id}' +  # noqa
                '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'subscriber/plans',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and save
        user = get_object_or_404(CustomUser, id=client_reference_id)
        user.stripeCustomerId = stripe_customer_id
        user.stripeSubscriptionId = stripe_subscription_id
        user.save()
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)


@csrf_exempt
def stripe_cancel(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if os.environ.get('DEVELOPMENT'):
        domain_url = os.getenv('DOMAIN_URL')
    else:
        domain_url = f"{ request.scheme }://{request.META['HTTP_HOST'] }/"
    try:
        stripe.Subscription.delete(
            request.user.stripeSubscriptionId,
            prorate=True,
            invoice_now=True
        )
        return redirect(f'{domain_url}subscriber/subscribed/{request.user.id}')
    except Exception as e:
        return messages.warning(request, e)
    return HttpResponse(status=200)
