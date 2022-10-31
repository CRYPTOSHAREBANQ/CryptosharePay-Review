from common_libraries.cryptoapis.cryptoapis_utils import CryptoApisUtils
from common_libraries.constants.comissions import REAL_RECEIVING_PERCENTAGE

from common_libraries.emails.email_client import EmailClient

from assets.models import Asset


class TransactionUtils:
    def __init__(self):
        pass

    def complete_transaction(self, transaction, api_key_object):
        ### TAX TAX TAX ###
        ### TAX TAX TAX ###
        
        print("PRE G", transaction.cryptocurrency_amount_received)
        receiving_amount = transaction.cryptocurrency_amount_received * REAL_RECEIVING_PERCENTAGE
        print("REAL G", receiving_amount)
        ### TAX TAX TAX ###
        ### TAX TAX TAX ###

        address_object = transaction.address_id
        cryptocurrency_object = address_object.cryptocurrency_id

        asset_object = Asset.objects.filter(api_key = api_key_object, cryptocurrency_id = cryptocurrency_object)
        if asset_object.exists():
            asset_object = asset_object.first()
            asset_object.amount += receiving_amount
            asset_object.save()
        else:
            asset_object = Asset.objects.create(
                api_key = api_key_object,
                type = cryptocurrency_object.type,
                amount = receiving_amount,
                cryptocurrency_id = cryptocurrency_object
            )
        
        # MAKE ADDRESS AVAILABLE
        cryptoapis_utils = CryptoApisUtils()
        error = cryptoapis_utils.release_address(address_object)
        if error is not None:
            return error

        # IF WITHDRAWAL ADDRESS WAS SPECIFIED
        error = cryptoapis_utils.withdraw_transaction_funds(transaction, cryptocurrency_object, receiving_amount)
        if error is not None:
            return error
        else:
            asset_object.amount -= receiving_amount
            asset_object.save()

        transaction.state = "COMPLETE"
        transaction.status = "COMPLETED"
        transaction.save()

        # SEND EMAIL
        email_client = EmailClient()
        email_client.complete_transaction(transaction)

        return None