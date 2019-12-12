import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { compose } from 'recompose';
import { SignUpLink } from '../SignUp';
import { withFirebase } from '../Firebase';
import * as ROUTES from '../../constants/routes';
import { PasswordForgetLink } from '../PasswordForget';
const SignInPage = () => (
  <div>
    <h1>SignIn</h1>
    <SignInForm />
    <PasswordForgetLink />
    <SignUpLink />
  </div>
);
const INITIAL_STATE = {
  email: '',
  password: '',
  error: null,
};
class SignInFormBase extends Component {
  constructor(props) {
    super(props);
    this.state = { ...INITIAL_STATE };
  }
  onSubmit = event => {
    const { email, password } = this.state;
    this.props.firebase
      .doSignInWithEmailAndPassword(email, password)
      .then(() => {
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
        this.props.firebase.db.collection('admin-logs').doc(datetime.toString()).set({
          "Action": "Sign In",
          "Email": email
        })
        this.setState({ ...INITIAL_STATE });
        this.props.history.push(ROUTES.HOME);
      })
      .catch(error => {
        this.setState({ error });
      });
    event.preventDefault();
  };
  onChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };
  render() {
    const { email, password, error } = this.state;
    const isInvalid = password === '' || email === '';
    return (
      <form onSubmit={this.onSubmit}>
        <input
          name="email"
          value={email}
          onChange={this.onChange}
          type="text"
          placeholder="Email Address"
        />
        <input
          name="password"
          value={password}
          onChange={this.onChange}
          type="password"
          placeholder="Password"
        />
        <button disabled={isInvalid} type="submit" value="sign in button">
          Sign In
        </button>
        {error && <p>{error.message}</p>}
      </form>
    );
  }
}
const SignInForm = compose(
  withRouter,
  withFirebase,
)(SignInFormBase);
export default SignInPage;
export { SignInForm };