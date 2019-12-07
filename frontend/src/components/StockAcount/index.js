import React from 'react';
import { AuthUserContext, withAuthorization } from '../Session';
import CreateStockAccount from '../../CreateStockAccount';
const StockAccountPage = props => (
    
      <div>
        <h1>Stock account number: {props.accountId}</h1>
        <CreateStockAccount></CreateStockAccount>
      </div>
  
);
export default StockAccountPage;
