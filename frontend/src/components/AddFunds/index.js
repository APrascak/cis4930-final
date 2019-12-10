import React, { Component } from 'react';
import { withFirebase } from '../Firebase';


class AddFunds extends Component {
    constructor(props) {
        super(props);
        
        this.state = {value: ''};
		this.handleChange = this.handleChange.bind(this);
    	this.handleSubmit = this.handleSubmit.bind(this);
      }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
	console.log("running" + this.props.accountId)
    this.props.firebase.users().doc(this.props.accountId).set({
            Money: parseInt(this.state.value) + parseInt(this.props.money) //or whatever money stockAccount starts off with
    });
    event.preventDefault();
  }
    
      render() {
        return (
			<div>
      <h2>Info from BuySell: {this.props.accountUpdate.action}, {this.props.accountUpdate.stock}, {this.props.accountUpdate.amnt}</h2>
				<h2>Account Funds</h2>
				<h4>Current Balance: {this.props.money}</h4>
				<h4>Add Funds to Account</h4>
          		<form onSubmit={this.handleSubmit}>
					<input
		        		type="text"
        				value={this.state.value} 
						onChange={this.handleChange}
					/>
					<input type="submit" value="Submit" />
				</form>
			</div>
        );
      }
    }

export default withFirebase(AddFunds);