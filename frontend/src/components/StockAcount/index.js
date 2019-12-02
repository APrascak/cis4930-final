import React from 'react';
import { AuthUserContext, withAuthorization } from '../Session';
const StockAccountPage = props => (
  <AuthUserContext.Consumer>
    {authUser => (
      <div>
        <h1>Stock account number: {props.accountId}</h1>
      </div>
    )}
  </AuthUserContext.Consumer>
);
const condition = authUser => !!authUser;
export default withAuthorization(condition)(StockAccountPage);
