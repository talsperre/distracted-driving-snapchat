# Annotation portal

A simple annotation portal designed to be used for annotation in this as well as other projects. The portal can easily be modifed as per the current needs.

1. Login and Registration
2. View video as soon as login, annotate. Only after complete annotation allow submission:-
3. Total videos annotated so far to show per user
4. An admin panel with a few representations/statistics of annotated data so far

# Pages
1. Homepage
2. Login form
3. Registration form followed by otp verification
4. dashboard with video and logout button
keep the html for each page in separate files.

# API
1. /register : Register a user. POST  
  Parameters:
      - email
      - password
      - confirmPassword
      - firstName
      - lastName      

  Response:
  - "Invalid email"/"passwords do not match"/"name must contain only alphabets"/"success"


2. /login : POST  
Parameters:
  - email
  - password

  Response:
  - "password does not match"/"success"

3. /fetchUserDetails : GET    
Response:
  - email
  - firstName
  - lastName
  - numAnnotated


# Frontend API calls being made
For all of the following if response is 200, successful. Anything else is error.
1. For sign up
fetch('http://localhost:8080/register', {
 method: 'POST',
 body: JSON.stringify({email: this.state.email, password:this.state.password}),
})

2. For OTP verification
fetch('http://localhost:8080/verifyOTP', {
 method: 'POST',
 body: JSON.stringify({confirmationCode: this.state.confirmationCode}),
})

3. For login
fetch('http://localhost:8080/register', {
 method: 'POST',
 body: JSON.stringify({email: this.state.email, password:this.state.password}),
})

4. For logout
fetch('http://localhost:8080/logout', {
 method: 'POST',
 body: JSON.stringify({email: this.state.email}),
})

5. For annotating a video
fetch('http://localhost:8080/annotate', {
 method: 'POST',
 body: JSON.stringify({email: this.state.email, videoID:this.state.videoID, dangerous: true, driving: false}),
})

For the following, return types specifically mentioned:-

6. For getting user details
fetch('http://localhost:8080/getUserDetails/<email>', {
 method: 'GET'),
})
return type is json :-
{
  email: string
  numAnnotated: int
}

7. For requesting a video
fetch('http://localhost:8080/getVideo', {
 method: 'POST',
 body: JSON.stringify({email: this.state.email}),
})
return type is json :-
{
  videoID: int
}
