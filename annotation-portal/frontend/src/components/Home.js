import React, { Component } from 'react';
import '../styles/Home.css'
import ViewVideos from './ViewVideos'

class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoggedIn: this.props.isLoggedIn,
    };
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Home</h1>
        </header>
        {
          this.state.isLoggedIn === false
          ? <div> <h2>Welcome to the annotation portal</h2>
            <h3>Please select an option from the menu bar above</h3> </div>
          : <ViewVideos />
        }

      </div>
    );
  }
}

export default Home;
