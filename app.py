# !pip install guardrails-ai
# !guardrails configure
# $env:PYTHONIOENCODING="utf-8"

# !guardrails hub install hub://guardrails/toxic_language
# !guardrails hub install hub://guardrails/nsfw_text
# !guardrails hub install hub://guardrails/sensitive_topics

from flask import Flask, request, jsonify
from flask_cors import CORS
from functions import *
import os
import json
from cv_data import *

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/cv_upload", methods=["POST"])
def cv_upload():
    if request.method == "POST":
        if "cv" in request.files:
            uploaded_file = request.files["cv"]
            session_id = request.form.get("session")

            print("1")
            # Get the filename and file extension
            filename = uploaded_file.filename
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()  # Convert to lowercase for comparison

            if file_extension == '.pdf':
                print(f"{filename} is a PDF file.")
                user_cv = f"{session_id}.pdf"
            elif file_extension == '.docx':
                print(f"{filename} is a Word file.")
                user_cv = f"{session_id}.docx"
            
            # return "Unsupported file format."
            # user_cv = f"{session_id}.pdf"
            uploaded_file.save(user_cv)
            # text = convert_pdf_to_text(f"./{user_cv}")
            banned_words = ["sex", "porn", "slut", "bitch", "play boy", "fuck", "fuckyou"]
            text, resultt = convert_pdf_to_text(f"./{user_cv}", banned_words)
            if resultt == False:
                return {"message": "input file exceed the file size Limit or file is not a cv"}, 413
            json_data = JSON(text)
            print("############################")
            print(json_data)
            update_data(json.dumps(json_data, indent=4), session_id)
            print(f"Data saved successfully ")
            os.remove(user_cv)
            return {"message": "CV uploaded"}, 200
        else:
            return {"message": "CV not found in request"}, 400
    else:
        return {"message": "only POST allowed"}


@app.route("/Updating_CV_content", methods=["POST"])
def Updating_CV_content():
    uploaded_file = request.files["cv"]
    user_id = request.form.get("mongoID")
    print("1")
    # Get the filename and file extension
    filename = uploaded_file.filename
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()  # Convert to lowercase for comparison

    if file_extension == '.pdf':
        print(f"{filename} is a PDF file.")
        user_cv = f"{user_id}.pdf"
    elif file_extension == '.docx':
        print(f"{filename} is a Word file.")
        user_cv = f"{user_id}.docx"

    # Save the uploaded file to the server
    uploaded_file.save(user_cv)
    #     return "File uploaded successfully."
    # else:
    #     return "No file part in the request."
    
    banned_words = ["sex", "porn", "slut", "bitch", "play boy", "fuck", "fuckyou"]
    text, resultt = convert_pdf_to_text(f"./{user_cv}", banned_words)
    # print ("$$$$$$$$$$$$$4",resultt)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@",text)
    if resultt == False:
        return {"message": "input file exceed the file size Limit or file is not a cv"}, 413
    text1 = JSON(text)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@",text1)

    # Remove the temporary PDF file
    # send_data = '"' + text1 + '"'
    os.remove(user_cv)

    # Update CV content in MongoDB
    result = update_cv_content(text1, user_id)
    if result:
        return {"message": "CV Content Updated Successfully"}, 200 
    else:
        return {"message": "An Error Occurred while updating CV content"}, 500


@app.route("/profile_building", methods=["POST"])
def profile():
    if request.method == "POST":
        session = request.form.get("session")  # Access 'ip' sent in the request data
        data = get_cv_data(session)

        if data:
            # variable = request.form.get("variable")
            # if variable is None:
            #     return {"message": "variable is missing in the request."}, 400
            # json_data = json_read(data)
            feed_back = profile_building(data)
            return {"message": feed_back}, 200

        else:
            return {"message": "The file does not exist."}, 200
    else:
        return {"message": "only post allowed"}, 200

@app.route("/cover_letter", methods=["POST"])
def coverletter():
    if request.method == "POST":
        session = request.form.get("session")
        # user_cv = f"{session}.json"
        # file_path = os.path.join("./", user_cv)
        data = get_cv_data(session)
        if data:
            r_name = request.form.get("r_name")
            company_name = request.form.get("company_name")
            company_address = request.form.get("company_address")
            job_description = request.form.get("job_description")

            if None in (r_name, company_name, company_address, job_description):
                return {"message": "Details are missing in the request."}, 400

            details = {
                "recipient_name": r_name,
                "company_name": company_name,
                "company_address": company_address,
                "job_description": job_description,
            }
            feed_back = cover_letter(data, details)

            try:
                # Clean the feedback to ensure it only contains valid JSON
                feedback_json = feed_back.strip()
                # Parse and return the JSON response
                return jsonify(json.loads(feedback_json)), 200
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
                print("Feedback received:", feed_back)
                return jsonify({"message": "Failed to decode JSON response.", "error": str(e), "response": feed_back}), 500

        else:
            return {"message": "The file does not exist in the folder."}, 200
    else:
        return {"message": "only post allowed"}, 200


@app.route("/advice_feedback", methods=["POST"])
def advice_feedback():
    if request.method == "POST":
        session = request.form.get("session")
        data = get_cv_data(session)
        print(data)
        if data:
            job_designation = request.form.get("job_designation")
            print(job_designation)
            if job_designation is None:
                return {"message": "Job Designation is missing in the request."}, 400

            feed_back = advice(data, job_designation)
            print(f"Feed Back: {feed_back}")
            score = score_calculator(data, job_designation)
            print(f"Score: {score}")

            if not feed_back:
                return {"message": "Feedback is empty."}, 400
            if not score:
                return {"message": "Score is empty."}, 400

            try:
                feed_back = json.loads(feed_back)
                score = json.loads(score)
            except json.JSONDecodeError as e:
                print("############################")
                return {"message": f"Invalid JSON: {e}"}, 400

            # Check if the expected keys are in the JSON objects
            if "data" not in feed_back:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                return {"message": "Missing 'data' in feedback."}, 400
            if "Eligibility_Score" not in score:
                print("**********************************")
                return {"message": "Missing 'Eligibility_Score' in score."}, 400

            response_data = {
                "feed_back": feed_back["data"],
                "score": score["Eligibility_Score"],
            }
            json_response = json.dumps(
                response_data, indent=4
            )  # indent for readability

            return json_response, 200
        else:
            return {"message": "The file does not exist in the folder."}, 200
    else:
        return {"message": "only post allowed"}, 200



@app.route("/interview_questions", methods=["POST"])
def interview_question():
    if request.method == "POST":
        # session = request.form.get("session")  # Access 'ip' sent in the request data
        job_description = request.form.get("job_description")
        print("2")
        if job_description is None:
            return {"message": "Description is missing in the request."}, 400
        feed_back = interview_questions(job_description)
        feed_back = feed_back.replace("\n", "")  # Replace '\n' with an empty string

        return feed_back, 200
    else:
        return {"message": "only post allowed"}, 200


@app.route("/CV_updation", methods=["POST"])
def cv_upd():
    if request.method == "POST":
        session = request.form.get("session")  # Access 'ip' sent in the request data
        data = get_cv_data(session)
        if data:
            job_designation = request.form.get("job_designation")

            if job_designation is None:
                return {"message": "Description is missing in the request."}, 400
            feed_back = CV_updation(data, job_designation)
            return feed_back, 200

        else:
            return {"message": "The file does not exist in the folder."}, 200
    else:
        return {"message": "only post allowed"}, 200

@app.route("/create_CV", methods=["POST"])
def cv_create():
    if request.method == "POST":
        request_data = request.json
        # plain = remove_symbols(request_data)

        print(request_data)
        new_cv = create_cv_with_ai(request_data)
        print(new_cv)
        return new_cv, 200

    else:
        return {"message": "only POST Method allowed"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", debug=True)