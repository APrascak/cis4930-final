import React from 'react';
import { PasswordForgetForm } from '../PasswordForget';
import PasswordChangeForm from '../PasswordChange';
import StockAccount from '../StockAcount';
import { AuthUserContext, withAuthorization } from '../Session';
const AccountPage = () => (
  <AuthUserContext.Consumer>
    {authUser => (
      <div>
        <h1>Account: {authUser.email}</h1>
        <h1>Account: {authUser.uid}</h1>
        <PasswordForgetForm />
        <PasswordChangeForm />
        <StockAccount accountId={authUser.uid + "one"}/>
        <StockAccount accountId={authUser.uid + "two"}/>
        <StockAccount accountId={authUser.uid + "three"}/>
      </div>
    )}
  </AuthUserContext.Consumer>
);
const condition = authUser => !!authUser;
export default withAuthorization(condition)(AccountPage);