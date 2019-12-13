import React, { Component } from 'react';
import { AuthUserContext, withAuthorization } from '../Session';
import BuySell from '../BuySell'


import CreateStockAccount from '../CreateStockAccount';
import UserList from '../UserList';
import { withFirebase } from '../Firebase';
class StockAccountPage extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      hasStockAccount: false,
      users: [],
      stockAccountMoney: 0};
  }

  componentDidMount() {

    this.setState({ loading: true });
    this.unsubscribe = this.props.firebase
      .users()
      .onSnapshot(snapshot => {
        let users = [];
        snapshot.forEach(doc =>
          users.push({ ...doc.data(), id: doc.id }),
        );
        this.setState({
          users,
          loading: false,
        });
        let accountId = this.props.accountId
			const index = this.state.users.findIndex(function(user, index){
				return user.id === accountId
      })
      if(index != -1)
      {
        this.setState({hasStockAccount: true});
      }
    if (this.state.users[index])
    {
      this.setState({stockAccountMoney: this.state.users[index].Money});
    }

    
    
    console.log(this.state.stockAccountMoney)
      });

      

  }

  componentWillUnmount() {
    this.unsubscribe();
  }

  

  render() {
    const hasStockAccount = this.state.hasStockAccount;
    let createStockAccount;
    if(hasStockAccount){
      createStockAccount = <div><BuySell accountId={this.props.accountId} money={this.state.stockAccountMoney}/></div>;
    }
    else{
      createStockAccount = <CreateStockAccount accountId={this.props.accountId} firebase={this.props.firebase}></CreateStockAccount>;
    }

     return (
      <div>
        <h1>Stock account</h1>
        {createStockAccount}
      </div>
     )
  }
  
}
export default withFirebase(StockAccountPage);
