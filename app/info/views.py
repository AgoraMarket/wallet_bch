from flask import jsonify
from app.info import info


# End Models


@info.route('/status', methods=['GET'])
def vendor_topbar_get_issues_count():
    """
    Gets status of wallet info
    :return:
    """
    return jsonify({
        "wallet_status": 'not yet set up',
    })
