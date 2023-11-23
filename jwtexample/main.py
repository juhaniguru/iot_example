import jwt
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

USERS = [
    {'id': 1, 'username': 'juhani', 'password': 'password'}
]


@app.route('/')
def hello():
    return "hello world"



@app.route('/api/v1/auth/account')
def get_account():
    bearer_token = request.headers.get('Authorization')
    bearer, _token = bearer_token.split(' ')

    decoded_jwt = jwt.decode(_token, "sdflkfsdjfsdlkjdsflsdfkjsflkj234l43k2j342lkj423l423kj432lk324j24l3kj423lk243", algorithms=["HS256"])
    account = None
    for user in USERS:
        if user['id'] == decoded_jwt['sub']:
            account = user
            break
    if account is None:
        return jsonify({'err': 'Unauthorized'}), 401
    return {'account': account}




@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # get username and password out of the request body
        request_body = request.get_json()
        for user in USERS:
            if user['username'] == request_body['username'] and user['password'] == request_body['password']:
                # create jwt here

                encoded_jwt = jwt.encode({'sub': user['id']},
                                         "sdflkfsdjfsdlkjdsflsdfkjsflkj234l43k2j342lkj423l423kj432lk324j24l3kj423lk243",
                                         algorithm="HS256")
                break
        return jsonify({'access_token': encoded_jwt})



if __name__ == '__main__':
    app.run(port=4000)
