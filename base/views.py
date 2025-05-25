
import uuid
from django.shortcuts import render , redirect
from .models import Transaction
import requests
from django.http import HttpResponse
from django.conf import settings


def checkout(request):
    tx_ref = f"tx-{uuid.uuid4()}"
    amount = 2000  # you can make this dynamic

    # Save transaction (optional but recommended)
    Transaction.objects.create(ref=tx_ref, amount=amount, status='pending')

    context = {
        "public_key": "FLWPUBK-7e15d7e29a41ecfe8d78a781aabfadf5-X",
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": "https://your-redirect.com/",
    }

    return render(request, "base/checkout.html", context)


def payment_callback(request):
    tx_ref = request.GET.get('tx_ref')
    status = request.GET.get('status')
    transaction_id = request.GET.get('transaction_id')

    if not tx_ref or not status:
        return HttpResponse("Missing tx_ref or status", status=400)

    try:
        transaction = Transaction.objects.get(ref=tx_ref)
    except Transaction.DoesNotExist:
        return HttpResponse("Transaction not found", status=404)

    if status != 'successful':
        transaction.status = 'failed'
        transaction.save()
        return redirect('/payment-cancelled/')  # or show your own failure page

    # Verify the transaction with Flutterwave
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json().get('data', {})

        if (
            data.get('status') == 'successful' and
            float(data.get('amount')) == float(transaction.amount) and
            data.get('currency') == transaction.currency
        ):
            transaction.status = 'paid'
            transaction.flutterwave_transaction_id = transaction_id
            transaction.save()
            return redirect('/payment-success/')  # your custom success page
        else:
            transaction.status = 'failed'
            transaction.save()
            return redirect('/payment-error/')  # mismatch in amount/currency

    except Exception as e:
        print(f"Verification error: {e}")
        return HttpResponse("Verification failed", status=500)


