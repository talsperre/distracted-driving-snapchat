import React, { Component } from 'react';
import '../styles/Logout.css'

class Logout extends Component {
  constructor(props) {
    super(props);

    this.state = {
      APIresponse: false,
      err: false,
    };
  }

  componentWIllUpdate () {
    // make API call to logout
    fetch('http://localhost:8080/logout', {
     method: 'POST',
     body: JSON.stringify({email: this.state.email}),
    })
      .then(response => {
        if(response.status >= 200 && response.status < 300) {
          this.setState({ APIresponse: true });
          this.props.logOut();
        } else {
          this.setState({err: true})
        }
      });

      this.props.logOut();
      this.setState({ APIresponse: true });
  }

  // plsLogOut () {
  //   this.props.logOut();
  //   this.setState({ APIresponse: true });
  //   return <div> Logged out </div>
  // }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Home</h1>
        </header>
        <h2>Logging you out...</h2>
        {
          this.state.APIresponse &&
            <h3>Successful! You've been logged out</h3>
        }
        {
          this.state.err &&
            <h3> ERROR! Could not logout. Please try again. </h3>
        }
      </div>
    );
  }
}

export default Logout;
