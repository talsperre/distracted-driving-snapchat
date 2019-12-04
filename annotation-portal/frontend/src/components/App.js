import React, { Component } from 'react';

import Home from './Home';
import Login from './Login';
import Signup from './Signup';
import NotFound from "./NotFound";
import Logout from "./Logout"
import '../styles/App.css'

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

class App extends Component {
  constructor() {
    super();

    this.state = {
      isLoggedIn: false,
      email: "",
    };
  }

  logIn(email) {
    this.setState({isLoggedIn: true, email: email});
  }

  logOut() {
    fetch('http://localhost:8080/logout', {
     method: 'POST',
     body: JSON.stringify({email: this.state.email}),
    })
      .then(response => {
        if(response.status >= 200 && response.status < 300) {
          this.setState({isLoggedIn: false, email: ""});
        }
      });
      // this.setState({isLoggedIn: false, email: ""});
  }

  render() {
    return (
      <div>
        <Router>
          <div>
            <nav className="navbar navbar-default">
              <div className="container-fluid">
                <div className="navbar-header">
                  <Link className="navbar-brand" to={'/'}>Snapchat Annotation</Link>
                </div>
                <ul className="nav navbar-nav">
                  <li><Link to={'/'}>Home</Link></li>
                </ul>
                {
                    this.state.isLoggedIn === false
                      ? ( <ul className="nav navbar-nav navbar-right"> <li><Link to={'/register'}>Register</Link></li>
                        <li><Link to={'/login'}>Login</Link></li> </ul>)
                      : (<ul className="nav navbar-nav navbar-right"><li><a onClick={this.logOut.bind(this)}>Logout</a></li></ul>)
                }
              </div>
            </nav>
            <Switch>
                 <Route exact path='/' component={() => <Home isLoggedIn={this.state.isLoggedIn} />} />
                 <Route exact path='/login' component={() => <Login logIn={this.logIn.bind(this)} isLoggedIn={this.state.isLoggedIn} />} />
                 <Route exact path='/logout' component={() => <Logout logOut={this.logOut.bind(this)} isLoggedIn={this.state.isLoggedIn} />} />
                 <Route exact path='/register' component={() => <Signup />} />
                 <Route component={NotFound} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
