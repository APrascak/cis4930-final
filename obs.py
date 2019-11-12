# OBS Authentication Program w/ Command line UI

import pyrebase

# Config location: Firebase console -> project settings -> general -> your apps
config = {
	"apiKey": "AIzaSyAy8Jl60TWPZPNIIilXPa7swc4f0yMHph4",
	"authDomain": "firestore-demo-3ebe9.firebaseapp.com",
	"databaseURL": "https://firestore-demo-3ebe9.firebaseio.com",
	"projectId": "firestore-demo-3ebe9",
	"storageBucket": "firestore-demo-3ebe9.appspot.com",
	"messagingSenderId": "175643772561"
}

# Initialize app connection and auth
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

print 'Welcome to OBS'
logged_in = False

while (not logged_in):
	print '1. Log in'
	print '2. Sign up'
	answer = input()
	if answer == 1:
		email = raw_input('Please enter your email:\n')
		password = raw_input("Please enter your password:\n")
		try:
			user = auth.sign_in_with_email_and_password(email,password)
		except:
			print 'Invalid username or password'
		else:
			print 'Successfully logged in!'
			print 'User token: ' + str(user['idToken'])
			logged_in = True
	elif answer == 2:
		email = raw_input('Please enter your email:\n')
		password = raw_input("Please enter your password:\n")
		if len(password) >= 8:
			user = auth.create_user_with_email_and_password(email,password)
			logged_in = True
		else:
			print "Password length must be greater than 7 characters."
	else: 
		print 'Invalid selection'

print '\n\n'

choice = -1
while (choice != 0):
	print 'Functions:'
	print '0. Exit Program'
	print '1. Get Account Information'
	print '2. View Stock Prices'
	print '3. Buy Stock'
	print '4. Sell Stock'
	choice = input()

	if choice == 1:
		print 'choice #: ' + str(choice)
		# Add account info implementation
	elif choice == 2:
		print 'choice #: ' + str(choice)
		# Add view stock price implementation
	elif choice == 3:
		print 'choice #: ' + str(choice)
		# Add buy stock implementation
	elif choice == 4:
		print 'choice #: ' + str(choice)
		# Add sell stock implementation

