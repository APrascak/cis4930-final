/*!

=========================================================
* Paper Dashboard React - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)

* Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

// reactstrap components
import { Card, CardHeader, CardBody, CardFooter, CardTitle, Row, Col, InputGroup,
  InputGroupText,
  InputGroupAddon,
  Input } from "reactstrap";
import {
  dashboard24HoursPerformanceChart,
  dashboardEmailStatisticsChart,
  dashboardNASDAQChart
} from "variables/charts.jsx";
import { Line, Pie } from "react-chartjs-2";


class Icons extends React.Component {
  render() {
    //const { email, password, error} = this.state;
    const isInvalid = false;
    return (
      <>
        <div className="content">
          <Row>
            <Col lg="4">
              <h4>Login</h4>
            </Col>
            <Col lg="4">
              <h4>Registration</h4>
            </Col>
          </Row>
          <Row>
            <Col lg="4">
              <form action="">
                <p>Email:</p>
                <inputGroup className="">
                <Input></Input>
                <p>Password:</p>
                <Input></Input>
                </inputGroup>
              </form>
            </Col>
            <Col lg="4">
              <form action="">
                <p>Email:</p>
                <inputGroup className="">
                <Input></Input>
                <p>Password:</p>
                <Input></Input>
                <p>Confirm Password:</p>
                <Input></Input>
                </inputGroup>
              </form>
            </Col>
          </Row>
        </div>
      </>
    );
  }
}

export default Icons;
