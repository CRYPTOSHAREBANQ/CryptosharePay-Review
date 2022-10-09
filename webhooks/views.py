from django.http import HttpResponse
from django.shortcuts import render

import json
from decimal import Decimal


from transactions.models import Transaction, TransactionBook ,TransactionIns
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network
from api_keys.models import Assets


# Create your views here.

def cryptoapis_confirmed_coin_transactions(request):
    pass

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


    receiving_cryptocurrency = Cryptocurrency.objects.get(
        blockchain_id = receiving_blockchain,
        network_id = receiving_network,
        symbol = response_data["unit"]
    )

    receiving_address = response_data["address"]
    receiving_address_object = Address.objects.get(
        address = receiving_address,
        cryptocurrency_id = receiving_cryptocurrency
    )
    

    new_transaction_in = TransactionIns.objects.create(
        external_transaction_id = response_data["transactionId"],
        amount = response_data["amount"],
        address_id = receiving_address_object,
        state = "COMPLETE",
        status = "CONFIRMED",
    )

    main_transaction = Transaction.objects.get(
        address_id = receiving_address_object,
        state = "OPEN",
        status = "PENDING"
    )
    main_transaction.cryptocurrency_amount_received += Decimal(response_data["amount"])
    main_transaction.save()

    new_transaction_book_registry = TransactionBook.objects.create(
        type = "IN",
        transaction_id = main_transaction,
        transaction_ins_id = new_transaction_in
    )

    ### <---------- END MAIN TRANSACTION PROCESS ----------> ###


    ### <---------- MISSING CODE HERE ----------> ###

    # MISSING TO VERIFY IF THE TRANSACTION IS COMPLETE

    api_key_object = main_transaction.api_key

    if main_transaction.cryptocurrency_amount_received >= main_transaction.cryptocurrency_amount:
        main_transaction.state = "COMPLETE"
        main_transaction.status = "CONFIRMED"
        main_transaction.save()

        asset_object = Assets.objects.filter(api_key = api_key_object, cryptocurrency_id = receiving_cryptocurrency)
        if asset_object.exists():
            asset_object = asset_object.first()
            asset_object.amount += main_transaction.cryptocurrency_amount_received
            asset_object.save()
        else:
            new_asset_object = Assets.objects.create(
                api_key = api_key_object,
                type = receiving_cryptocurrency.type,
                amount = main_transaction.cryptocurrency_amount_received,
                cryptocurrency_id = receiving_cryptocurrency
            )
        

        # MISSING TO SEND THE CONFIRMATION EMAIL TO THE USER

    ### <---------- MISSING CODE HERE ----------> ###

    return HttpResponse(status=200)
