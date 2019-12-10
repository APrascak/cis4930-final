import app from 'firebase/app';
import 'firebase/auth';
import 'firebase/firestore';

const config = {
    apiKey: "AIzaSyAy8Jl60TWPZPNIIilXPa7swc4f0yMHph4",
    authDomain: "firestore-demo-3ebe9.firebaseapp.com",
    databaseURL: "https://firestore-demo-3ebe9.firebaseio.com",
    projectId: "firestore-demo-3ebe9",
    storageBucket: "firestore-demo-3ebe9.appspot.com",
    messagingSenderId: "175643772561",
  };

  function getDocument(db) {
    // [START get_document]
    let cityRef = db.collection('UserMoney').doc('wpXsdFVu8bMt2A593UEijxkANI93one');
    let getDoc = cityRef.get()
      .then(doc => {
        if (!doc.exists) {
          console.log('No such document!');
        } else {
          console.log('Document data:', doc.data());
        }
      })
      .catch(err => {
        console.log('Error getting document', err);
      });
    // [END get_document]
  
    return getDoc;
  }

  class Firebase {
    constructor() {
      app.initializeApp(config);

      this.auth = app.auth();
      this.fieldValue = app.firestore.FieldValue;
      this.db = app.firestore();
    }
    
    doCreateUserWithEmailAndPassword = (email, password) =>
    this.auth.createUserWithEmailAndPassword(email, password);

    doSignInWithEmailAndPassword = (email, password) =>
    this.auth.signInWithEmailAndPassword(email, password);

    doSignOut = () => this.auth.signOut();

    doPasswordReset = email => this.auth.sendPasswordResetEmail(email);
    doPasswordUpdate = password =>
    this.auth.currentUser.updatePassword(password);

    onAuthUserListener = (next, fallback) =>
    this.auth.onAuthStateChanged(authUser => {
      if (authUser) {
        this.user(authUser.uid)
          .get()
          .then(snapshot => {
            const dbUser = snapshot.data();
            // default empty roles
            if (!dbUser.roles) {
              dbUser.roles = {};
            }
            // merge auth and db user
            authUser = {
              uid: authUser.uid,
              email: authUser.email,
              emailVerified: authUser.emailVerified,
              providerData: authUser.providerData,
              ...dbUser,
            };
            next(authUser);
          });
      } else {
        fallback();
      }
    });
   // *** User API ***
   user = uid => this.db.doc('UserMoney');
   //users = () => this.db.collection('wpXsdFVu8bMt2A593UEijxkANI93one');
   users = () => this.db.collection('UserMoney');

  //  getUserMoney = () => 
  //   this.users()
  //   .get()
  //   .then(querySnapshot => {
  //     const data = querySnapshot.docs.map(doc => {console.log(doc.id, '=>', doc.data());});
  //     //console.log("is this working");
  //     //console.log(querySnapshot.docs);
  //     //console.log(data);
  //     //this.setState({ users: data });
  //   });
   // *** Message API ***
   message = uid => this.db.doc(`messages/${uid}`);
   messages = () => this.db.collection('messages');

   
  }
  export default Firebase;