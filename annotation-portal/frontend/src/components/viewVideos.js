import React, { Component } from 'react';
import { Button } from "react-bootstrap";

import '../styles/ViewVideos.css'

class ViewVideos extends Component {
  constructor(props) {
    super(props);

    this.state = {
      APIresponse: true,
      APIresponse2: false,
      err: false,
      videoEnded: false,
      driving: 0,
      dangerous: 0,
      videoID: "",
    }
  }

  reqNewVideo() {
    const request = new Request('http://127.0.0.1:8080/people/', {method:'POST', body: JSON.stringify({email: this.state.email})});
    fetch(request)
      .then(response => response.json())
        .then(data => this.setState({videoID: data.videoID}));
  }

  componentDidMount () {
    // make first API call here
    this.reqNewVideo();

  }
  handleSubmit = event => {

    // make second API call here

    fetch('http://localhost:8080/annotate', {
     method: 'POST',
     body: JSON.stringify({email: this.state.email, videoID: this.state.videoID}),
    })
      .then(response => {
        if(response.status >= 200 && response.status < 300) {
          this.setState({APIresponse2: true});
        }
      });

    if (this.state.APIresponse2) {
      this.reqNewVideo();
    } else {
      this.setState({err: true})
    }

  }

  handleChange = event => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  validateForm() {
    return this.state.videoEnded;
  }

  render() {
    return (
      <div className="ViewVideos">
          <h3> Please watch the entire video. Only then will you be able to submit the form. </h3>
        {
          this.state.APIresponse &&
          <div>
          <video controls onEnded={() => this.setState({videoEnded: true})}>
            <source src="https://media.w3.org/2010/05/sintel/trailer.mp4"/>
          </video>

          <form onSubmit={this.handleSubmit}>
            <label>Is this video driving related?</label>
            <div className="radio">
              <label><input type="radio" name="driving" value="1" onChange={this.handleChange} />Yes</label>
            </div>
            <div className="radio">
            <label><input type="radio" name="driving" value="0" onChange={this.handleChange} />No</label>
            </div>
            <br />
            <label>Is this video dangerous?</label>
            <div className="radio">
              <label><input type="radio" name="dangerous" value="1" onChange={this.handleChange} />Yes</label>
            </div>
            <div className="radio">
            <label><input type="radio" name="dangerous" value="0" onChange={this.handleChange} />No</label>
            </div>

            <Button
              block
              bsSize="large"
              disabled={!this.validateForm()}
              type="submit"
            >
              Submit
            </Button>
          </form>
          </div>

        }
        {
          this.state.err &&
          <h4> Error, please reload. </h4>
        }



      </div>
    );
  }
}

export default ViewVideos;
