from flask import jsonify
from app.scripts import\
    account_checker,\
    wallet_checkincomming,\
    wallet_deletewalletwork,\
    wallet_generateaddresses,\
    wallet_getnewaddress,\
    wallet_send
from app import app


@app.route('/', methods=['GET'])
def get_wallet_status():
    """
    Gets the count of vendor order issues.  Notification bar at top
    :return:
    """

    return jsonify({
        "wallet_status": 'Bitcoin RPC is Online',
    })

@app.route('/deletework', methods=['GET'])
def delete_work():
    """
    This will delete work
    :return:
    """
    
    wallet_deletewalletwork.main()
    
    return jsonify({
        "status": 'Deleted Work',
    })
    
@app.route('/generateaddresses', methods=['GET'])
def generate_addresses():
    """
    This will generate addresses if it gets low or ignore if enough
    :return:
    """
    
    wallet_generateaddresses.main()
    
    return jsonify({
        "status": 'Generated Addresses',
    })
    
    
@app.route('/send', methods=['GET'])
def send_coin():
    """
    This will activiate the script to send coin
    :return:
    """
    
    wallet_send.main()
    
    return jsonify({
        "status": 'sent coin',
    })

@app.route('/recieve', methods=['GET'])
def recieve_coin():
    """
     This will activiate the script to check for incomming bitcoin
    :return:
    """
    wallet_checkincomming.main()
    
    return jsonify({
        "status": 'sent coin',
    })


@app.route('/checkaccounts', methods=['GET'])
def check_accounts():
    """
    This will check accounts to make sure no empty addresses
    :return:
    """
    
    account_checker.main()
    
    return jsonify({
        "status": 'Checked Accounts',
    })

