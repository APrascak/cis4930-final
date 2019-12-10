import React, { Component } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Navigation from '../Navigation';
import { JsonToTable } from "react-json-to-table";
import { withFirebase } from '../Firebase';
import { compose } from 'recompose';

const Admin = () => (
    <div>
      <h1>Admin Dashboard</h1>
      <AdminDashboard />
    </div>
);

class AdminDashboardBase extends Component {

  constructor(props) {
    super(props)
  }

  state = { logData: {} }

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
        this.setState({ logData }) // Sets state with queried results
      })

  // Render: table
  // Uses JsonToTable so that logs are displayed regardless of log attributes
  render() {
    return ( 
      <div>
        <JsonToTable json={this.state.logData}/> 
      </div>
    );
  }

}

const AdminDashboard = compose(withFirebase)(AdminDashboardBase)
export default Admin;
export { AdminDashboard };