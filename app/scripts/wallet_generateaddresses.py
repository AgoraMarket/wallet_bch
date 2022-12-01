
from app import db
import requests
import json
from walletconfig import url
from app.classes.wallet_bch import Bch_WalletAddresses



def callforaddress():

    # standard json header
    headers = {'content-type': 'application/json'}

    # the method/params
    rpc_input = {
        "method": "getnewaddress",
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "1.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
        url,
        data=json.dumps(rpc_input),
        headers=headers,
    )

    # the response in json format
    response_json = response.json()
    print(response_json)
    return response_json


def main():
    # query amount addresses that are not uses
    get_available_addresses = db.session \
        .query(Bch_WalletAddresses) \
        .filter(Bch_WalletAddresses.status == 0) \
        .count()

    # see if less than 50
    if get_available_addresses >= 50:
        print(f"We have {get_available_addresses} addresses available still.  No need to run")
    else:
        # make 100 new addresses
        for f in range(10):

            # call the rpc
            newwalletaddress = callforaddress()

            # if error isnt present
            if newwalletaddress["result"].startswith('bitcoincash'):
                # get the new address
                the_address = newwalletaddress["result"]

                # add to db addresses
                walletadd = Bch_WalletAddresses(
                    bchaddress=the_address,
                    status=0,
                )

                db.session.add(walletadd)

        db.session.commit()


if __name__ == '__main__':
    main()
