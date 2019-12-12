import React from 'react';
import { Link } from 'react-router-dom';
import SignOutButton from '../SignOut';
import * as ROUTES from '../../constants/routes';
import { AuthUserContext } from '../Session';
import 'bootstrap/dist/css/bootstrap.min.css'
import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Button } from 'react-bootstrap';

const Navigation = () => (
  <div>
    <AuthUserContext.Consumer>
      {authUser =>
        authUser ? <NavigationAuth /> : <NavigationNonAuth />
      }
    </AuthUserContext.Consumer>
  </div>
);

// Navbar: authorized users
const NavigationAuth = () => (
  <Navbar bg="dark" variant="dark" className="justify-content-between">
    <Navbar.Brand href="#">
      <img
        alt=""
        src="/logo.svg"
        width="30"
        height="30"
        className="d-inline-block align-top"
      />{' '}
      Online Banking Service
    </Navbar.Brand>
    <Nav>
      <Nav.Link href={ROUTES.LANDING} variant="success">
        Landing
      </Nav.Link>
      <Nav.Link href={ROUTES.HOME}>
        Home
      </Nav.Link>
      <Nav.Link name="navAccount" href={ROUTES.ACCOUNT}>
        Account
      </Nav.Link>
    </Nav>
    <SignOutButton />
  </Navbar>
);

// Navbar: un-authorized users
const NavigationNonAuth = () => (
  <Navbar bg="dark" variant="dark" className="justify-content-between">
    <Navbar.Brand href="#">
      <img
        alt=""
        src="/logo.svg"
        width="30"
        height="30"
        className="d-inline-block align-top"
      />{' '}
      React Bootstrap
    </Navbar.Brand>
    <Nav>
      <Nav.Link href={ROUTES.LANDING}>
        Landing
      </Nav.Link>
      <Nav.Link href={ROUTES.SIGN_IN}>
        Sign In
      </Nav.Link>
    </Nav>
    <SignOutButton />
  </Navbar>
);
export default Navigation;