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
    //console.log(this.props)
  }

  state = { logData: {} }



  // logData = {
  //   "Logs": [
  //     // Empty Array to hold Firestore information
  //   ]
  // }

  test = this.props.firebase.db.collection('admin-logs')
    .get()
    .then(snapshot => {
      const logData = {
        "Logs": [

        ]
      }
      console.log("TESTING")
      console.log(logData)
      snapshot.forEach(doc => {
        logData.Logs.push(doc.data())
      })
      this.setState({ logData })
      this.status = true
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

  status = false

  render() {
    console.log('YEET')
    console.log(this.testData)
    console.log(this.state.logData)
    console.log(this.status)
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