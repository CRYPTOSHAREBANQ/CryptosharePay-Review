from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import json
from decimal import Decimal


from transactions.models import Transaction, TransactionBook ,TransactionIns, TransactionOuts
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network
from assets.models import Asset


# Create your views here.

@csrf_exempt
def cryptoapis_confirmed_coin_transactions(request):

    if ("Transfer-Encoding" in request.headers) and (request.headers["Transfer-Encoding"] == "chunked"):
        request_reader = request.META.get('wsgi.input')

        # bpayload = request_reader.stream.read1()  # UNCOMMENT FOR LOCAL TESTING ENVIRRONMENT
        bpayload = request_reader.read() #UNCOMMENT FOR PRODUCTION ENVIRONMENT
    else:
        bpayload = request.body

    payload = bpayload.decode("utf-8")

    start = payload.index("{")
    end = payload.rindex("}") + 1

    response = json.loads(payload[start:end])
    response_data = response["data"]["item"]

    receiving_blockchain = Blockchain.objects.get(blockchain_id = response_data["blockchain"])
    receiving_network = Network.objects.get(network_id = response_data["network"])

    ### <---------- STARTS MAIN TRANSACTION PROCESS ----------> ###

    transaction_cryptocurrency = Cryptocurrency.objects.get(
        blockchain_id = receiving_blockchain,
        network_id = receiving_network,
        symbol = response_data["unit"]
    )

    transaction_address = response_data["address"]
    transaction_address_object = Address.objects.get(
        address = transaction_address,
        cryptocurrency_id = transaction_cryptocurrency
    )

    if response_data["direction"] == "incoming":

        new_transaction_in = TransactionIns.objects.create(
            external_transaction_id = response_data["transactionId"],
            amount = response_data["amount"],
            address_id = transaction_address_object,
            completed_datetime = timezone.now(),
            state = "COMPLETE",
            status = "CONFIRMED",
        )

        try:
            main_transaction = Transaction.objects.get(
                address_id = transaction_address_object,
                state = "PENDING",
                status = "WAITING_FOR_DEPOSIT"
            )
        except:
            return HttpResponse(status=200)

        main_transaction.cryptocurrency_amount_received += Decimal(response_data["amount"])
        main_transaction.save()

        new_transaction_book_registry = TransactionBook.objects.create(
            type = "IN",
            transaction_id = main_transaction,
            transaction_ins_id = new_transaction_in
        )

        ### <---------- END MAIN TRANSACTION PROCESS ----------> ###


        ### <---------- MISSING CODE HERE ----------> ###

        api_key_object = main_transaction.api_key

        if main_transaction.cryptocurrency_amount_received >= main_transaction.cryptocurrency_amount:
            main_transaction.state = "COMPLETE"
            main_transaction.status = "CONFIRMED"
            main_transaction.save()

            asset_object = Asset.objects.filter(api_key = api_key_object, cryptocurrency_id = transaction_cryptocurrency)
            if asset_object.exists():
                asset_object = asset_object.first()
                asset_object.amount += main_transaction.cryptocurrency_amount_received
                asset_object.save()
            else:
                new_asset_object = Asset.objects.create(
                    api_key = api_key_object,
                    type = transaction_cryptocurrency.type,
                    amount = main_transaction.cryptocurrency_amount_received,
                    cryptocurrency_id = transaction_cryptocurrency
                )
            
            # MAKE ADDRESS AVAILABLE

            transaction_address_object.api_key = None
            transaction_address_object.status = "AVAILABLE"
            transaction_address_object.save()

            # MISSING TO SEND THE CONFIRMATION EMAIL TO THE USER
    elif response_data["direction"] == "outgoing":
        new_transaction_in = TransactionOuts.objects.create(
            external_transaction_id = response_data["transactionId"],
            amount = response_data["amount"],
            address_id = transaction_address_object,
            completed_datetime = timezone.now(),
            state = "COMPLETE",
            status = "CONFIRMED",
        )

    ### <---------- MISSING CODE HERE ----------> ###

    return HttpResponse(status=200)
