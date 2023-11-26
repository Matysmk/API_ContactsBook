# Postman simple API testing

This project was builded to practise simple API testing using most common endpoints such as: GET, POST, PUT, PATCH, DELETE. There is a small database, which consists of 1 table and 4 columns. However, it can be modified on your own and used as a subject of learning API testing.

- The code has been written in Python and its database library SQLite.
- All test cases has been prepared manually and then executed with Postman and Newman to execute collection and generate html report.
- To provide CI/CD integration I used Jenkins.

# How to use:

1. Clone this repository.
2. Run local server with command "python main.py".
3. Open up Postman.

# Endpoints:

1. Add contact:

- Endpoint: POST /api/contacts
- Params: Use json raw format including: first_name, last_name, city and phone_number. Remember, value cannot be empty!
- Expected message:
  "message": "Contact added successfully",
  "contactId": {number of contactId}
- Expected request response: Status 201 created or 400 Bad Request.

2. Get contacts list:

- Endpoint: GET /api/contacts
- Params: None
- Expected message:
  Status 200 OK / 404 Not Found

3. Get single contact

- Endpoint: Get /api/contacts/:id
- Params: id
- Expected message:
  Status 200 OK / 404 Not Found

4. Update single contact information

- Endpoint: Patch /api/contacts/:id
- Params: id
  Use json raw format including for example: first_name
- Expected message:
  "message": "Contact updated successfully"
  Status 200 OK / 500 Internal Server Error.

4. Update contact

- Endpoint: PUT /api/contacts/:id
- Params:
  id
  Use json raw format including: first_name, last_name, city and phone_number
- Expected message:
  "message": "Contact updated successfully"
  Status 204 No content / 400 Bad request.

5. Delete contact

- Endpoint: DELETE /api/contacts/:id
- Params:
  id
- Expected message:
  "message": "Contact deleted successfully"
  Status 200 OK / 404 Not Found.

# Newman usage:

Create collection of your tests and then:

npm install -g newman
Run Newman: newman run mycollection.json

To generate HTML report install:
npm install -g newman-reporter-htmlextra
Run: newman run mycollection.json -r htmlextra
