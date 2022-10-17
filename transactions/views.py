from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import ApiKey
from cryptocurrency.models import Cryptocurrency, Blockchain, Network
from transactions.models import Transaction, TransactionBook, TransactionIns, TransactionOuts
from digital_currency.models import DigitalCurrency

from transactions.serializers import TransactionSerializer, TransactionsSerializer

# from rest_framework import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response  import Response
from rest_framework import status

from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils


