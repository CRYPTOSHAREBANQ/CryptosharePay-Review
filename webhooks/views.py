from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import json
from decimal import Decimal


from transactions.models import Transaction, TransactionBook ,TransactionIns, TransactionOuts
from cryptocurrency.models import Address, Blockchain, Cryptocurrency, Network, StaticAddress
from assets.models import Asset

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.transactions.transactions_utils import TransactionUtils
from common_libraries.cryptoapis.cryptoapis import CryptoApis
from common_libraries.constants.comissions import REAL_RECEIVING_PERCENTAGE

from rest_framework.response  import Response


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

        ### CAN BE OPTIMIZED ###
        ### CAN BE OPTIMIZED ###
        ### CAN BE OPTIMIZED ###

        try:
            main_transaction = Transaction.objects.get(
                address_id = transaction_address_object,
                state = "PENDING",
                status = "WAITING_FOR_DEPOSIT"
            )
        except:
            try:
                static_address_object = StaticAddress.objects.get(
                    address_id = transaction_address_object,
                    type = "DEPOSIT_ADDRESS",
                    status = "IN_USE"
                )

                main_transaction = Transaction.objects.create(
                    api_key = transaction_address_object.api_key,
                    type = "STATIC_DEPOSIT",
                    description = "Deposit to static address",
                    cryptocurrency_amount = response_data["amount"],
                    address_id = static_address_object.address_id,
                    expiration_datetime = None,
                    state = "COMPLETED",
                    status = "COMPLETED",
                )
            except:
                #MISSING TO SET UP AN ERROR LOG
                return HttpResponse(status=500)

        
        ### CAN BE OPTIMIZED ###
        ### CAN BE OPTIMIZED ###
        ### CAN BE OPTIMIZED ###

        main_transaction.cryptocurrency_amount_received += Decimal(response_data["amount"])
        main_transaction.save()

        new_transaction_book_registry = TransactionBook.objects.create(
            type = "IN",
            transaction_id = main_transaction,
            transaction_ins_id = new_transaction_in
        )

        ### <---------- END MAIN TRANSACTION PROCESS ----------> ###

        api_key_object = main_transaction.api_key

        if main_transaction.cryptocurrency_amount_received >= main_transaction.cryptocurrency_amount:

            transaction_utils = TransactionUtils()

            error = transaction_utils.complete_transaction(main_transaction, api_key_object)
            if error is not None:
                response_object = {
                    "status": "ERROR",
                    "message": error
                }
                return Response(response_object, status=500)

    elif response_data["direction"] == "outgoing":
        new_transaction_in = TransactionOuts.objects.create(
            external_transaction_id = response_data["transactionId"],
            amount = response_data["amount"],
            address_id = transaction_address_object,
            completed_datetime = timezone.now(),
            state = "COMPLETE",
            status = "CONFIRMED",
        )

    return HttpResponse(status=200)


@csrf_exempt
def cryptoapis_confirmed_token_transactions(request):

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

    token_type = response_data["tokenType"]
    token_data = response_data["token"]
    
    receiving_blockchain = Blockchain.objects.get(blockchain_id = response_data["blockchain"])
    receiving_network = Network.objects.get(network_id = response_data["network"])

    ### <---------- STARTS MAIN TRANSACTION PROCESS ----------> ###

    transaction_cryptocurrency = Cryptocurrency.objects.get(
        blockchain_id = receiving_blockchain,
        network_id = receiving_network,
        symbol = token_data["symbol"],
        type = token_type
    )

    transaction_address = response_data["address"]
    transaction_address_object = Address.objects.get(
        address = transaction_address,
        cryptocurrency_id = transaction_cryptocurrency
    )

    if response_data["direction"] == "incoming":

        new_transaction_in = TransactionIns.objects.create(
            external_transaction_id = response_data["transactionId"],
            amount = token_data["amount"],
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
            #MISSING TO SET UP AN ERROR LOG

            return HttpResponse(status=200)

        main_transaction.cryptocurrency_amount_received += Decimal(token_data["amount"])
        main_transaction.save()

        new_transaction_book_registry = TransactionBook.objects.create(
            type = "IN",
            transaction_id = main_transaction,
            transaction_ins_id = new_transaction_in
        )

        ### <---------- END MAIN TRANSACTION PROCESS ----------> ###

        api_key_object = main_transaction.api_key

        if main_transaction.cryptocurrency_amount_received >= main_transaction.cryptocurrency_amount:

            transaction_utils = TransactionUtils()

            error = transaction_utils.complete_transaction(main_transaction, api_key_object)
            if error is not None:
                response_object = {
                    "status": "ERROR",
                    "message": error
                }
                return Response(response_object, status=500)

            # MISSING TO SEND THE CONFIRMATION EMAIL TO THE USER
    elif response_data["direction"] == "outgoing":
        new_transaction_in = TransactionOuts.objects.create(
            external_transaction_id = response_data["transactionId"],
            amount = token_data["amount"],
            address_id = transaction_address_object,
            completed_datetime = timezone.now(),
            state = "COMPLETE",
            status = "CONFIRMED",
        )

    return HttpResponse(status=200)
