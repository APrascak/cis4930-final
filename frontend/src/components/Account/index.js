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
        <PasswordForgetForm />
        <PasswordChangeForm />
        <StockAccount data="1"/>
        <StockAccount data="2"/>
        <StockAccount data="3"/>
        <StockAccount data="4"/>
        <StockAccount data="5"/>
      </div>
    )}
  </AuthUserContext.Consumer>
);
const condition = authUser => !!authUser;
export default withAuthorization(condition)(AccountPage);