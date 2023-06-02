from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from decimal import Decimal
import datetime
from dateutil.relativedelta import relativedelta

from accounts.models import Account, Country
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency, Blockchain, Network, StaticAddress
from transactions.models import AutomatedTransaction
from digital_currency.models import DigitalCurrency


# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.object_responses.object_responses import GenericCORSResponse
from common_libraries.constants.cryptocurrency import CRYPTOCURRENCY_NETWORKS
from common_libraries.transactions.transactions_utils import TransactionUtils
from common_libraries.emails.email_client import EmailClient
from common_libraries.general.general_utils import get_next_event_datetime


class CreateAutomatedPayoutDigitalToCrypto(APIView):
    def post(self, request):
        data = request.data["data"]
        headers = request.headers


        #MISSING TO VERIFY ALL THIS INPUTS INTO MIDDLEWARE

        api_key = headers.get("X-API-Key", None)

        description = data["description"]
        frecuency = data["frecuency"]
        scheduled_day = data["scheduled_day"]

        digital_currency_code = data["digital_currency_code"]
        digital_currency_amount = data["digital_currency_amount"]
        cryptocurrency_code = data["cryptocurrency_code"]
        cryptocurrency_blockchain_id = data["cryptocurrency_blockchain_id"]

        funds_source_type = data.get("funds_source_type", "DEPOSIT_ADDRESS")

        receiver_address = data["receiver_address"]
        unique_deposit_address = data.get("unique_deposit_address", False)

        customer_email = data.get("customer_email", None)
        customer_phone = data.get("customer_phone", None)


        if funds_source_type != "DEPOSIT_ADDRESS":
            return Response(
                {
                    "status": "ERROR",
                    "error": "This funds source type is currently not supported yet"
                }, status = 409)

        """
            STEPS TO CREATE A AUTOMATED PAYOUT TRANSACTION

            GET API KEY OBJECT
            GET DIGITAL CURRENCY OBJECT
            DEFINE TRANSACTION TYPE
            GENERATE ADDRESS
            CREATE TRANSACTION      
        """

        api_key_object = ApiKey.objects.get(api_key = api_key)

        digital_currency_object =  DigitalCurrency.objects.get(digital_currency_id = digital_currency_code)

        # print(api_key_object.type, cryptocurrency_code)
        network_object = Network.objects.get(network_id = CRYPTOCURRENCY_NETWORKS[api_key_object.type][cryptocurrency_code])
        blockchain_object = Blockchain.objects.get(blockchain_id = cryptocurrency_blockchain_id)

        cryptocurrency_object = Cryptocurrency.objects.get(
            blockchain_id = blockchain_object,
            network_id = network_object,
            symbol = cryptocurrency_code
        )

        #TODO MISSING TO VERIFY IF A STATIC ADDRESS IS ALREADY AVAILABLE FOR THIS CRYPTOCURRENCY AND API KEY
        if unique_deposit_address:
            type = "AUTOMATED_FUNDS_SOURCE"
        else:
            type = "GENERIC_STATIC"

        if funds_source_type == "DEPOSIT_ADDRESS":
            # GENERATE ADDRESS
            cryptoapis_utils = CryptoApisUtils()
            static_address_object, error = cryptoapis_utils.generate_static_address(cryptocurrency_object, api_key_object, unique = unique_deposit_address, type = type)
            if error is not None:
                return GenericCORSResponse(
                    response = {
                        "status": "ERROR",
                        "message": error
                        },
                    status = 400).get_response()

        next_event_datetime = get_next_event_datetime(frecuency, scheduled_day)            
        
        next_event_datetime = next_event_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        new_transaction = AutomatedTransaction.objects.create(
            api_key = api_key_object,
            status = "ACTIVE",
            description = description,
            type = "PAYOUT_DIGITAL_TO_CRYPTO",
            frecuency = frecuency,
            scheduled_day = scheduled_day,
            funds_source_type = funds_source_type,
            funds_source_address_object = static_address_object,
            digital_currency_id = digital_currency_object,
            digital_currency_amount = digital_currency_amount,
            cryptocurrency_id = cryptocurrency_object,
            receiver_address = receiver_address,
            client_email = customer_email,
            client_phone = customer_phone,
            next_event_datetime = next_event_datetime
        )

        response_object = {
            "status": "SUCCESS",
            "message": "Automated Transaction created successfully",
            "data": {
                "transaction_id": new_transaction.transaction_id,
                "funds_source_address": static_address_object.address_id.address if funds_source_type == "DEPOSIT_ADDRESS" else None,
                "next_event_datetime": new_transaction.next_event_datetime,
                "creation_timestamp": new_transaction.creation_datetime.timestamp(),
                "next_event_datetime_timestamp": new_transaction.next_event_datetime.timestamp(),
            }
        }

        return Response(response_object, status=200)

    
class CancelAutomatedPayout(APIView):
    def post(self, request):
        headers = request.headers
        data = request.data["data"]

        api_key = headers.get("X-API-Key", None)
        api_key_object = ApiKey.objects.get(api_key = api_key)

        transaction_id = data["transaction_id"]
        
        transaction = AutomatedTransaction.objects.get(api_key = api_key_object, transaction_id = transaction_id)

        transaction_utils = TransactionUtils()
        error = transaction_utils.cancel_automated_transaction(transaction)
        if error is not None:
            response_object = {
                "status": "ERROR",
                "message": error
            }
            return Response(response_object, status=503)

        email_client = EmailClient()
        email_client.cancel_automated_transaction(transaction, str(transaction.api_key.user_id.email))

        response_object = {
            "status": "SUCCESS",
            "message": f"Automated Transaction {transaction_id} cancelled successfully"
        }

        return Response(response_object, status=200)