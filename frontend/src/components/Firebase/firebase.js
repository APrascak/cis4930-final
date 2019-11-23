import app from 'firebase/app';
import 'firebase/auth';

const config = {
    apiKey: "AIzaSyAy8Jl60TWPZPNIIilXPa7swc4f0yMHph4",
    authDomain: "firestore-demo-3ebe9.firebaseapp.com",
    databaseURL: "https://firestore-demo-3ebe9.firebaseio.com",
    projectId: "firestore-demo-3ebe9",
    storageBucket: "firestore-demo-3ebe9.appspot.com",
    messagingSenderId: "175643772561",
  };

  class Firebase {
    constructor() {
      app.initializeApp(config);

      this.auth = app.auth();
    }
    doCreateUserWithEmailAndPassword = (email, password) =>
    this.auth.createUserWithEmailAndPassword(email, password);

    doSignInWithEmailAndPassword = (email, password) =>
    this.auth.signInWithEmailAndPassword(email, password);

    doSignOut = () => this.auth.signOut();

    doPasswordReset = email => this.auth.sendPasswordResetEmail(email);
  doPasswordUpdate = password =>
    this.auth.currentUser.updatePassword(password);
  }
  export default Firebase;