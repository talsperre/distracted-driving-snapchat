import React, { Component } from "react";
import { Button, HelpBlock, FormGroup, FormControl, ControlLabel } from "react-bootstrap";

import "../styles/Login.css";

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password: "",
      APIresponse: false,
      err: false,
    };
  }

  validateForm() {
    return this.state.email.length > 0 && this.state.password.length > 0;
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  handleSubmit = event => {
    event.preventDefault();

    // make API call here
    // fetch('http://localhost:8080/register', {
    //  method: 'POST',
    //  body: JSON.stringify({email: this.state.email, password:this.state.password}),
    // })
    //   .then(response => {
    //     if(response.status >= 200 && response.status < 300) {
    //       this.setState({ APIrepsonse: true });
    //     } else {
    //       this.setState({err: true})
    //     }
    //   });

    this.props.logIn(this.state.email);
    this.setState({APIresponse: true});
  }

  render() {
    return (
      <div className="Login">
      {
        this.state.APIresponse === true
        ? <h4>Successfully logged in, please go back to home </h4>
        :  <div>
          {
          this.state.err === true
          ? <HelpBlock>Error encountered, please refresh your page</HelpBlock>
          : <form onSubmit={this.handleSubmit}>
              <FormGroup controlId="email" bsSize="large">
                <ControlLabel>Email</ControlLabel>
                <FormControl
                  autoFocus
                  type="email"
                  value={this.state.email}
                  onChange={this.handleChange}
                />
              </FormGroup>
              <FormGroup controlId="password" bsSize="large">
                <ControlLabel>Password</ControlLabel>
                <FormControl
                  value={this.state.password}
                  onChange={this.handleChange}
                  type="password"
                />
              </FormGroup>

              <Button
                block
                bsSize="large"
                disabled={!this.validateForm()}
                type="submit"
              >
                Login
              </Button>
              {
                this.state.err &&
                <HelpBlock>Invalid email ID or password</HelpBlock>
              }

            </form>
            }
            </div>

      }
      </div>
    );
  }
}

export default Login
