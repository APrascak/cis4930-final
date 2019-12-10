import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import { withFirebase } from '../Firebase';
import * as ROUTES from '../../constants/routes';

class UserList extends Component {
  constructor() {
    super();

    this.state = {
      loading: false,
      userId:[],
      users: [],
    };
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
        console.log(this.state.users);
      });

      console.log(this.state.users);

  }

  componentWillUnmount() {
    this.unsubscribe();
  }

  returnsomething() {
      return 1;
  }

  render() {
    const { users, loading } = this.state;

    return (
      <div>
        <h2>Users</h2>
        {loading && <div>Loading ...</div>}
        <ul>
          {users.map(user => (
            <li key={user.id}>
              <span>
                <strong>ID:</strong> {user.id}
              </span>
              <span>
                <strong>Money:</strong> {user.Money}
              </span>              
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default withFirebase(UserList);