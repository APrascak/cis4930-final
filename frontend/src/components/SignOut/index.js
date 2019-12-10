import React, { Component } from 'react';
import { withFirebase } from '../Firebase';
import * as firebase from 'firebase';
import { compose } from 'recompose';
import { Link, withRouter } from 'react-router-dom';


const SignOutButton = ({ firebase }) => (
  <SignOutBtn />
);

class SignOutBase extends Component {

  constructor(props) {
    super(props)
  }

  onSubmit = event => {

    var currentdate = new Date(); 
        var datetime = currentdate.getDate() + "-"
                        + (currentdate.getMonth()+1)  + "-" 
                        + currentdate.getFullYear() + " @ "  
        if (currentdate.getHours() < 10) {
          datetime += "0" + currentdate.getHours() + ":"
        } else {
          datetime += currentdate.getHours() + ":"
        }
        if (currentdate.getMinutes() < 10) {
          datetime += "0" + currentdate.getMinutes() + ":"
        } else {
          datetime += currentdate.getMinutes() + ":"
        }
        if (currentdate.getSeconds() < 10) {
          datetime += "0" + currentdate.getSeconds()
        } else {
          datetime += + currentdate.getSeconds()
        }
        console.log(datetime)
        this.props.firebase.db.collection('admin-logs').doc(datetime.toString()).set({
          "Action": "Sign Out",
          "Email": firebase.auth().currentUser.email
        })
        this.props.firebase.doSignOut()

  }

  render() {
    return (
      <button type="button" onClick = {this.onSubmit}>
        Sign Out
      </button>
    )
  }

}

const SignOutBtn = compose(
  withRouter,
  withFirebase,
)(SignOutBase);
export default withFirebase(SignOutButton);