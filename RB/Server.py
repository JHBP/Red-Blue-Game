import httplib, errno
import random, string
listener = None
gameId = ''
gameUid = ''


def usage():
    print 'Available commands:'
    print '-- config'
    print '-- start'
    print '-- start NODES ROUNDS TIME <SEED>'
    print '-- join GAME_ID'

# Wrapper function for any tasks that should only run on startup
def init():
    server, id = config()
    print 'Type "?" for a list of commands'
    return server, id

# TODO: Stop any active listeners if server is reconfigured
def config():
    host_default = '127.0.0.1'
    port_default = '4040'
    player_id_default = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    host = raw_input('Enter the server (no port) [' + host_default + ']: ')
    port = raw_input('Enter the port [' + port_default + ']: ')
    player_id = raw_input("Enter your personal ID: ")
    if not host.strip():
        host = host_default
    if not port.strip():
        port = port_default
    if not player_id.strip():
        player_id = player_id_default
    server = host + ':' + str(port)

    print 'Set connection URL to', server

    return server, player_id

# Makes a request to the given server + URL with the given method, body, and headers,
# and returns the response object and response body in a tuple. The body is returned
# as well so that the connection can be closed as soon as possible. Not intended for
# long polling.
def sendRequest(server, method, url, body, headers):
    try:
        conn = httplib.HTTPConnection(server)
        conn.request(method, url, body, headers)
        response = conn.getresponse()
        responseBody = response.read()
        conn.close()
        return (response, responseBody)
    except httplib.InvalidURL, err:
        print 'Error: ', err.message # usually means invalid/nonnumeric port
    except IOError, err:
        if (errno.errorcode[err.errno] == 'ENOEXEC'):
            print 'Error: Cannot reach the given URL. It may be incorrect, or your internet may be down.'
        elif (errno.errorcode[err.errno] == 'ECONNREFUSED'):
            print 'Error: Connection refused. Your URL may be incorrect, or the server may be down.'
        else:
            print IOError, err
    except Exception, err:
        return None
        raise


def requestMove(server, id, game_id):
    S_MOVE_RECEIVED = 200
    S_ERROR = 404

    reqHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = sendRequest(server, 'GET', '/game/' + game_id + '/'+id,'{}', reqHeaders)

    resStatus = response[0].status
    if resStatus == S_MOVE_RECEIVED:
        return response
    elif resStatus == S_ERROR:
        print("Error occured when requesting move")
    return None

def submitMove(server, id, game_id, selected_node):
    S_MOVE_SUBMITTED = 200
    S_ERROR = 404

    reqBody = '{"node": ' + selected_node + '}'
    reqHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = sendRequest(server, 'POST', '/game/' + game_id + '/' + id, reqBody, reqHeaders)
    resStatus = response[0].status
    if resStatus == S_MOVE_SUBMITTED:
        return response
    elif resStatus == S_ERROR:
        print("Error occurred when submitting move")
    return response

def startGame(server, details, id):
    S_GAME_STARTED = 201
    S_PARAM_ERROR = 400
    S_RATE_LIMIT = 406

    try:
        reqBody = '{"nodes":' + str(int(details['nodes']))
        reqBody += ', "rounds":' + str(int(details['rounds']))
        reqBody += ', "time":' + str(int(details['time']))
        reqBody += ', "prob":' + str(float(details['prob']))
        if details['seed']:
            reqBody += ', "seed":' + str(int(details['seed']))
        reqBody += '}'
    except ValueError, err:
        print ValueError, err
        return
    except Exception, err:
        print Exception, err
        raise
    reqHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = sendRequest(server, 'POST', '/game/', reqBody, reqHeaders)

    if not response:
        return

    resHeaders = response[0].getheaders()
    resStatus = response[0].status
    resBody = response[1]

    if resStatus == S_GAME_STARTED:
        for (key, value) in resHeaders:
            if key == 'location':
                newGameId = value.split('/')[2]
                print 'Game with id "' + newGameId +'" created, joining...'
                return joinGame(server, {'game_id': newGameId}, id), newGameId
    elif resStatus == S_PARAM_ERROR:
        print resBody.split('\n', 1)[0]
    elif resStatus == S_RATE_LIMIT:
        print 'Error: too many requests (Enhance Your Calm)'
    else:
        print 'Unexpected error:', resStatus, response[0].reason
        raise Exception

def joinGame(server, details, id):

    S_GAME_JOINED = 200 # will be 200 (spec doc definition)
    S_GAME_NOT_FOUND = 404
    S_GAME_FULL = 423

    # TODO: suffix poll url with 'join/'
    reqBody = '{"id": "' + id + '"}'
    reqHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = sendRequest(server, 'POST', '/game/' + details['game_id'] + '', reqBody, reqHeaders)

    if not response:
        return

    resStatus = response[0].status

    if resStatus == S_GAME_JOINED:
        gameId = details['game_id']
        gameUid = '<unimplemented>'
        print ('Game with id "' + gameId + '" joined.')
        return response
        # print resBody # dumps the game state, sent by server
    elif resStatus == S_GAME_NOT_FOUND:
        print 'Error: No game with id "' + details['game_id'] + '"'
    elif resStatus == S_GAME_FULL:
        print 'Error: Game with id "' + details['game_id'] + '" already full'
    else:
        print 'Unexpected error:', resStatus, response[0].reason
        raise Exception
    return None


if __name__ == "__main__":
    main()