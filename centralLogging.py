from firebase import firebase
DBConn = firebase.FirebaseApplication('https://firestore-demo-3ebe9.firebaseio.com/', None)

def userLogs(token, timeStamp, isLogin):
    data_to_upload = {
        'Token' : token,
        'Time Stamp' : timeStamp,
        'isLogin' : isLogin
    }
    DBConn.post('/CentralLogging/UserLogs/', data_to_upload)
    
def userFunds(token, timeStamp, balanceChange):
    data_to_upload = {
        'Token' : token,
        'Time Stamp' : timeStamp,
        'balance Change' : balanceChange
    }
    DBConn.post('/CentralLogging/UserFunds/', data_to_upload)