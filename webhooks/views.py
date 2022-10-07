from django.http import HttpResponse
from django.shortcuts import render
import json
from transactions.models import Transaction, TransactionBook ,TransactionIns
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network


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

    new_transaction_book_registry = TransactionBook.objects.create(
        type = "IN",
        transaction_id = main_transaction,
        transaction_ins_id = new_transaction_in
    )

    ### <---------- MISSING CODE HERE ----------> ###

    # MISSING TO VERIFY IF THE TRANSACTION IS COMPLETE

    # MISSING TO CLOSE THE TRANSACTION IF IT IS COMPLETE

    # MISSING TO CREDIT ASSETS TO THE USER ACCOUNT

    ### <---------- MISSING CODE HERE ----------> ###

    return HttpResponse(status=200)
