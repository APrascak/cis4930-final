import React, { Component } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Navigation from '../Navigation';
import { JsonToTable } from "react-json-to-table";
import { withFirebase } from '../Firebase';
import { compose } from 'recompose';
import 'bootstrap/dist/css/bootstrap.min.css'
import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Button, Container } from 'react-bootstrap';

const Admin = () => (
    <Container>
      <h1>Admin Dashboard</h1>
      <AdminDashboard />
    </Container>
);

class AdminDashboardBase extends Component {

  constructor(props) {
    super(props)
  }

  state = { logData: {}, transactionLogs: {} }
  

  // Retrieves admin logs from database
  // Updates state after retrieval
  test = this.props.firebase.db.collection('admin-logs')
    .get()
      .then(snapshot => {
        const logData = { // Formats admin logs into new variable
          "Logs": [

          ]
        }
        snapshot.forEach(doc => {
          var info = doc.data()
          info['TimeStamp'] = doc.id
          console.log(info)
          logData.Logs.push(info) // Adds individual documents to logData
        })
        this.setState({ logData: logData}) // Sets state with queried results
        console.log(this.state.transactionLogs)
      })

  test1 = this.props.firebase.db.collection('transaction-logs')
  .get()
    .then(snapshot => {
      const transactionLogs = { // Formats admin logs into new variable
        "Transactions": [

        ]
      }
      snapshot.forEach(doc => {
        var info = doc.data()
        info['TimeStamp'] = doc.id
        console.log(info)
        transactionLogs.Transactions.push(info) // Adds individual documents to logData
      })
      this.setState({ transactionLogs: transactionLogs })
    })

  // Render: table
  // Uses JsonToTable so that logs are displayed regardless of log attributes
  render() {
    return ( 
      <div>
        <JsonToTable json={this.state.transactionLogs}/>
        <JsonToTable json={this.state.logData}/> 
      </div>
    );
  }

}

const AdminDashboard = compose(withFirebase)(AdminDashboardBase)
export default Admin;
export { AdminDashboard };