import hvac
import os
import psycopg2

CA = 'ContaAzul'
IE = 'IntegrationEngine'
AV = 'Avalanche'
VAULT_CREDENTIAL_KEY = 'vaultCredentialKey'
DB_HOST = 'databaseHost'
DB_NAME = 'databaseName'

cons = {}
db_data = {}
db_data[CA] = {VAULT_CREDENTIAL_KEY : 'database/creds/contaazul-datareader', DB_HOST : 'readdb-adhoc.prod.contaazul.local', DB_NAME : 'contaazul'}
db_data[IE] = {VAULT_CREDENTIAL_KEY : 'database/creds/integration-engine-datareader', DB_HOST : 'integrations-rds.prod.contaazul.local', DB_NAME :'integrationengine'}
db_data[AV] = {VAULT_CREDENTIAL_KEY : 'database/creds/avalanche-datareader', DB_HOST : 'avalanche-rds.prod.contaazul.local', DB_NAME :'avalanche'}

def authenticate() :
    client = hvac.Client()
    client.auth.github.login(token = os.environ['GITHUB_TOKEN'])
    return client

def isAuthenticated(client) :
    return client.is_authenticated()

def connectToDB(connectionName, host, db, username, passphrase) :
    global cons
    print("Gerando conexão  com o host " + host)
    con = psycopg2.connect(host = host, database = db, user = username, password = passphrase)
    cons[connectionName] = con

def executeSQL(db,sql) :
    cur = cons[db].cursor()
    cur.execute(sql)
    return cur.fetchall()

def closeDBCons() :
    for con in cons :
        cons[con].close()

def generateNecessaryConnections(client) :
    for db in db_data :
        data = db_data[db]
        credential = client.read(data[VAULT_CREDENTIAL_KEY])['data']
        user = credential['username']
        password = credential['password']
        connectToDB(IE, data[DB_HOST], data[DB_NAME], user, password)


def run() :
    client = authenticate()
    if isAuthenticated(client) :
        generateNecessaryConnections(client)
        response = executeSQL(IE, 'select * from credential where tenant_id = 1531370;')
        print(type(response))
        print(response)
        closeDBCons()




run()