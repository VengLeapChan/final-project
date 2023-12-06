from flask import Flask, jsonify, request
from functools import reduce
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@mysql:3306/mydatabase'
db = SQLAlchemy(app)

# employees = [
#     {"EmployeeID": 1, "FirstName": "John", "LastName": "Doe",
#         "EmailAddress": "john.doe@peoplesuite.com", "Country": "US"},
#     {"EmployeeID": 2, "FirstName": "Jane", "LastName": "Doe",
#         "EmailAddress": "jane.doe@peoplesuite.com", "Country": "GB"},
#     {"EmployeeID": 3, "FirstName": "June", "LastName": "Doe",
#         "EmailAddress": "june.doe@peoplesuite.com", "Country": "AU"}
# ]

class Employees(db.Model):
    EmployeeID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    EmailAddress = db.Column(db.String(255), nullable=False, unique=True)
    Country = db.Column(db.String(2), nullable=False)

    def to_dict(self):
        return {
            'EmployeeID': self.EmployeeID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'EmailAddress': self.EmailAddress,
            'Country': self.Country
        }


@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'GET':
        employees = Employees.query.all()
        returnEmployees = [x.to_dict() for x in employees]
        return jsonify(returnEmployees), 200
    elif request.method == 'POST':

        employeeData = request.json
        newEmployee = Employees(
            FirstName=employeeData['FirstName'],
            LastName=employeeData['LastName'],
            EmailAddress=employeeData['EmailAddress'],
            Country=employeeData['Country']
        )
        db.session.add(newEmployee)
        db.session.commit()
        return jsonify(newEmployee.to_dict()), 201
        # # gets the rest body and save it
        # employeeData = request.json 

        # # finds the employe with the maximum employee ID
        # maxEmpDict = reduce(
        #     lambda x, y: x if x["EmployeeID"] > y["EmployeeID"] else y, employees)

        # # find the new max ID
        # newEmpId = maxEmpDict["EmployeeID"] + 1
        # employeeData['EmployeeID'] = newEmpId

        # # add it to the list
        # employees.append(employeeData)
        # return jsonify(employeeData), 201


# @app.route('/employees/<int:employee_id>', methods=['GET'])
# def get_employee(employee_id):

#     # filters for the employee
#     emp = list(filter(lambda x: x["EmployeeID"] == employee_id, employees))
#     if emp == []:

#         # if employee not found, return error message
#         return jsonify({"error": "Employee not found"}), 404

#     # returns the employee
#     return jsonify(emp[0]), 200


if __name__ == '__main__':
    app.run(debug=True)
