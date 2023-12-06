from flask import Flask, jsonify, request
from functools import reduce

app = Flask(__name__)

employees = [
    {"EmployeeID": 1, "FirstName": "John", "LastName": "Doe",
        "EmailAddress": "john.doe@peoplesuite.com", "Country": "US"},
    {"EmployeeID": 2, "FirstName": "Jane", "LastName": "Doe",
        "EmailAddress": "jane.doe@peoplesuite.com", "Country": "GB"},
    {"EmployeeID": 3, "FirstName": "June", "LastName": "Doe",
        "EmailAddress": "june.doe@peoplesuite.com", "Country": "AU"}
]

maxEmpID = 3


@app.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'GET':
        returnEmployees = []
        for emp in employees:
            newEmp = {'EmployeeID': emp["EmployeeID"], 'FirstName': emp["FirstName"],
                      'LastName': emp["LastName"], "EmailAddress": emp["EmailAddress"]}
            returnEmployees.append(newEmp)
        return jsonify(returnEmployees), 200
    elif request.method == 'POST':
        # gets the rest body and save it
        employeeData = request.json

        # finds the employe with the maximum employee ID
        maxEmpDict = reduce(
            lambda x, y: x if x["EmployeeID"] > y["EmployeeID"] else y, employees)

        # find the new max ID
        newEmpId = maxEmpDict["EmployeeID"] + 1
        employeeData['EmployeeID'] = newEmpId

        # add it to the list
        employees.append(employeeData)
        return jsonify(employeeData), 201


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):

    # filters for the employee
    emp = list(filter(lambda x: x["EmployeeID"] == employee_id, employees))
    if emp == []:

        # if employee not found, return error message
        return jsonify({"error": "Employee not found"}), 404

    # returns the employee
    return jsonify(emp[0]), 200


if __name__ == '__main__':
    app.run(debug=True)
