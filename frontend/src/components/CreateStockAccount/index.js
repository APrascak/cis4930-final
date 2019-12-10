import React, { Component } from 'react';
import { withFirebase } from '../Firebase';


class CreateStockAccount extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
          users: []
          };
      }

    handleClick() {
        console.log('this is:', this);
        console.log(this.props.accountId);
        this.props.firebase.users().doc(this.props.accountId).set({
            Money: 0 //or whatever money stockAccount starts off with
          });
      }
    
      render() {
        return (
          <button onClick={(e) => this.handleClick(e)}>
            Create Stock Account
          </button>
        );
      }
    }

export default withFirebase(CreateStockAccount);