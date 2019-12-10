import React, { Component } from 'react';

class CreateStockAccount extends Component {
    handleClick() {
        console.log('this is:', this);
      }
    
      render() {
        // This syntax ensures `this` is bound within handleClick
        return (
          <button onClick={(e) => this.handleClick(e)}>
            Click me
          </button>
        );
      }
    }

export default CreateStockAccount;