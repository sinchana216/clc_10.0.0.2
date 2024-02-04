from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/studentdb'
mongo = PyMongo(app)

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Details</title>
</head>
<body>
  <h1>Student Details</h1>
  <form id="studentForm" method="post" action="{{ url_for('students') }}">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    <br>
    <label for="age">Age:</label>
    <input type="number" id="age" name="age" required>
    <br>
    <label for="grade">Grade:</label>
    <input type="text" id="grade" name="grade" required>
    <br>
    <button type="submit">Add Student</button>
  </form>

  <div id="studentList"></div>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const studentList = document.getElementById('studentList');

      const fetchStudents = async () => {
        const response = await fetch('{{ url_for("students") }}');
        const students = await response.json();

        studentList.innerHTML = '<h2>Student List</h2>';
        students.forEach((student) => {
          const studentDiv = document.createElement('div');
          studentDiv.innerHTML = `<p>Name: ${student.name}, Age: ${student.age}, Grade: ${student.grade}</p>`;
          studentList.appendChild(studentDiv);
        });
      };

      fetchStudents();
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        grade = request.form['grade']

        mongo.db.students.insert_one({'name': name, 'age': age, 'grade': grade})

        return 'Student added successfully'

    elif request.method == 'GET':
        students = list(mongo.db.students.find())
        return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
