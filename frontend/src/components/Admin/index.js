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
    console.log(this.props)
  }

  logData = {
    "Logs": [
      
    ]
  }

  test = this.props.firebase.db.collection('admin-logs')
    .get()
    .then(snapshot => {
      snapshot.forEach(doc => {
        this.logData.Logs.push(doc.data())
      })
    })

  myJson = {
    "Student": { name: "Jack", email: "jack@xyz.com" },
    "Student id": 888,
    "Sponsors": [
      { name: "john", email: "john@@xyz.com" },
      { name: "jane", email: "jane@@xyz.com" }
    ]
  };

  testData = {
    "Logs": [
      { UID: "alex", Action: "Log in", Email: "alex@gmail.com", Timestamp: "Nov 11 2019"},
      { UID: "paul", Action: "Register", Email: "paul@gmail.com", Timestamp: "Nov 13 2019"}
    ]
  }

  render() {
    console.log('YEET')
    console.log(this.testData)
    console.log(this.logData)
    return ( 
      <div>
        <JsonToTable json={this.logData.Logs}/>
      </div>
    )
  }
}
const AdminDashboard = compose(withFirebase)(AdminDashboardBase)

export default Admin;
export { AdminDashboard };