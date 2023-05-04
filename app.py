
from flask import Flask, request, render_template
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

app = Flask(__name__)


credential = ClientSecretCredential('a48cca56-e6da-484e-a814-9c849652bcb3', 'ae20b393-5b1d-4c35-b3b3-a4333f8def72', 'LKk8Q~IVilFiQSWrVcPdQWPVPWGlMt2OCBeZwdm0')

secret_client = SecretClient(vault_url='https://vault-store-054oi85.vault.azure.net/', credential=credential)

def insert_record(record):
    secret_client.set_secret(record['name'], record['value'], 'application/json')
    
def get_record(key):
    return secret_client.get_secret(key).value


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        key = get_record(username)
        if key==password:
            return 'Login successfull', 200
        else:
            return 'Incorrect Login', 400
    else:
        return render_template('sample.html')
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    insert_record({'name': username, 'value': password})
    return 'Inserted into keyvault', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
