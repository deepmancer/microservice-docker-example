from flask import Flask, request, jsonify
from .application.student import add_student, modify_student, delete_student, get_student_information, \
    get_all_students_information
from .data_access import database

app = Flask(__name__)


@app.route('/student', methods=['POST'])
def api_add_student():
    data = request.json
    try:
        response = add_student(data['name'], data['age'], data['education_level'])
        return jsonify({"message": response.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/student', methods=['PUT'])
def api_modify_student():
    data = request.json
    try:
        response = modify_student(data['student_id'], data['name'], data['age'], data['education_level'])
        return jsonify({"message": response.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/student', methods=['DELETE'])
def api_delete_student():
    data = request.json
    try:
        response = delete_student(data['student_id'])
        return jsonify({"message": response.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/student', methods=['GET'])
def api_get_student_information():
    data = request.json
    try:
        student_info = get_student_information(data['student_id'])
        return jsonify(student_info.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route('/students', methods=['GET'])
def api_get_all_students_information():
    try:
        students_info = get_all_students_information()
        return jsonify([s.to_dict() for s in students_info]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True)
