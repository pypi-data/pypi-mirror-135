# SIMPLE PYTHON JSON FORMAT 
The repository contain a script to format your python response in a correct JSON format using the standard HTTP response codes. Well suitable to backend applications with REST API building concept in mind.

**Install the ngobot-json package**

`pip install ngobot-json`

**import the ngobot-json package**

`from ngobot_json.pyresponse import JsonResponse`

**1. Success Response**

you can simply return json successful response format in this way.

_e.g._

`response = JsonResponse()

print(response.Success())
`

_Output:_


`{
"status":200,
"message":"Successful",
"data":{
"status":200,
"message":"ok",
"reason":"Successful"
}
}`

You can modify the json success response format by passing two arguments: (1) the data to return as response and (2) the keyword indicator "success" to activate success response format.

_e.g. User Account Created._

`

task = "User Account successfully created"

response = JsonResponse(task, "success")

print(response.Created())

`

_Output:_

`
{
"status":201,
"message":"Created Successfully",
"data":{
"status":200,
"message":"ok",
"reason":"User Account successfully created"
}
}
`
_e.g. Process completed successfully_


`task = "The Process is successfully completed"

response = JsonResponse(task, "success")

print(response.Success())`



Output:


`{"status": 200, "message": "Successful", "data": {"status": 200, "message": "ok", "reason": "The Process is successfully completed"}}
`

**2. Error Response**

The error response follows the same pattern of the success modify response, but has a different keyword argument "error" to activate the error response format:

_e.g._

`task = "Invalid username and password"

response = JsonResponse(task, "error")

print(response.Unauthorized())`

_Output:_

`{
"status":401,
"message":"Unauthorized",
"data":{
"status":422,
"message":"Unprocessable Entity",
"reason":"Invalid username and password"
}
}`



**3. Adding External json return from another function or database.**
note that in this section we use keyword "data" to activate the json format with external json file.

_e.g._ 


`task = {
"status":201,
"message":"Created Successfully",
"data":{
"status":200,
"message":"ok",
"reason":"User Account successfully created"
}
}

response = JsonResponse(task, "data")

print(response.Success())`


Output:

`{"status": 200, "message": "Successful", "data": {"status": 201, "message": "Created Successfully", "data": {"status": 200, "message": "ok", "reason": "User Account successfully created"}}}
`



**4. List of All the supported HTTP codes functions to call.**

comming soon.




