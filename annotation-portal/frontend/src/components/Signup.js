import React, { Component } from "react";
import {
  HelpBlock,
  FormGroup,
  FormControl,
  ControlLabel
} from "react-bootstrap";
import LoaderButton from "../components/LoaderButton";
import "../styles/Signup.css";

export default class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      email: "",
      password: "",
      confirmPassword: "",
      confirmationCode: "",
      newUser: null,
      done: false,
      err: false,
    };
  }

  validateForm() {
    return (
      this.state.email.length > 0 &&
      this.state.password.length > 0 &&
      this.state.password === this.state.confirmPassword
    );
  }

  validateConfirmationForm() {
    return this.state.confirmationCode.length === 6 && this.state.confirmationCode.match(/^[0-9]+$/) != null;
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  handleSubmit = async event => {
    event.preventDefault();

    this.setState({ isLoading: true });

    // Make 1st API call here
    fetch('http://localhost:8080/register', {
     method: 'POST',
     body: JSON.stringify({email: this.state.email, password:this.state.password}),
    })
      .then(response => {
        if(response.status >= 200 && response.status < 300) {
          this.setState({ newUser: "test" });
          this.setState({submitted: true});
        } else {
          this.setState({err: true})
        }
      });

    this.setState({ isLoading: false });
  }

  handleConfirmationSubmit = async event => {
    event.preventDefault();

    this.setState({ isLoading: true });
    // Make 2nd API call here
    fetch('http://localhost:8080/verifyOTP', {
     method: 'POST',
     body: JSON.stringify({confirmationCode: this.state.confirmationCode}),
    })
      .then(response => {
        if(response.status >= 200 && response.status < 300) {
          this.setState({done: true});
        } else {
          this.setState({err: true})
        }
      });

  }

  renderConfirmationForm() {
    return (
      <form onSubmit={this.handleConfirmationSubmit}>
        <FormGroup controlId="confirmationCode" bsSize="large">
          <ControlLabel>Confirmation Code</ControlLabel>
          <FormControl
            autoFocus
            type="tel"
            value={this.state.confirmationCode}
            onChange={this.handleChange}
          />
          <HelpBlock>Please check your email for the code.</HelpBlock>
        </FormGroup>
        <LoaderButton
          block
          bsSize="large"
          disabled={!this.validateConfirmationForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Verify"
          loadingText="Verifying…"
        />
      </form>
    );
  }

  renderForm() {
    return (
      <form onSubmit={this.handleSubmit}>
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
        <FormGroup controlId="confirmPassword" bsSize="large">
          <ControlLabel>Confirm Password</ControlLabel>
          <FormControl
            value={this.state.confirmPassword}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <LoaderButton
          block
          bsSize="large"
          disabled={!this.validateForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Signup"
          loadingText="Signing up…"
        />
      </form>
    );
  }

  render() {
    return (
      <div className="Signup">
      {
        this.state.err !== true
        ? <div>
          {
          this.state.done === false
          ?  (
            <div>
            {this.state.newUser === null
              ? this.renderForm()
              : this.renderConfirmationForm()}
            </div>
            )
          :
              <div className="done">
                  <HelpBlock>Registration complete, please login.</HelpBlock>
              </div>
          }
          </div>
        : (
          <div className="done">
              <HelpBlock>An error has been encountered, please refresh the page.</HelpBlock>
          </div>
          )
      }

      </div>
    );
  }
}
