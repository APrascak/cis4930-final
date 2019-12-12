  
import React from 'react';
import { PasswordForgetForm } from '../PasswordForget';
import PasswordChangeForm from '../PasswordChange';
import StockAccount from '../StockAcount';
import { AuthUserContext, withAuthorization } from '../Session';

import UserList from '../UserList';
const AccountPage = () => (
  <AuthUserContext.Consumer>
    {authUser => (
      <div>
        <h1>Account: {authUser.email}</h1>
        <PasswordForgetForm />
        <PasswordChangeForm />

        <br/>
        <hr/>       
        <StockAccount accountId={authUser.uid + "one"}/>
        <hr/>       
        <StockAccount accountId={authUser.uid + "two"}/>
        <hr/>       

        <StockAccount accountId={authUser.uid + "three"}/>
      </div>
    )}
  </AuthUserContext.Consumer>
);
const condition = authUser => !!authUser;
export default withAuthorization(condition)(AccountPage);