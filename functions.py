import os
from openai import OpenAI
import pdfplumber
import json
import re
from dotenv import load_dotenv
import docx

load_dotenv()
# python -m spacy download en_core_web_sm
####################################################
####################################################
####################################################
####################################################
####################################################

api_key = os.getenv("api_key")
client = OpenAI(api_key=api_key)

def remove_symbols(data):
    if isinstance(data, dict):
        # Initialize an empty list to store plain text values
        plain_text_values = []

        # Iterate through the values of the dictionary
        for value in data.values():
            # Convert the value to string and remove symbols using regex
            plain_text = re.sub(r"[^\w\s]", "", str(value))
            plain_text_values.append(plain_text)

        # Join the plain text values into a single string
        plain_text_string = " ".join(plain_text_values)

        return plain_text_string
    else:
        return "Invalid input: expecting dictionary"


def interview_questions(user_input):
    questions = []
    while len(questions) < 10:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a technical interview questions generator. Read the following job description carefully:
                    {user_input}
                    Generate exactly 10 unique and non-empty technical questions based on the job description. Each question should be on a new line without numbering.
                    """
                }
            ],
        )
        response_message = response.choices[0].message.content.strip()

        # Split the response by new lines and filter out any empty strings
        new_questions = [q for q in response_message.split('\n') if q.strip()]
        questions.extend(new_questions)
        questions = questions[:10]  # Ensure no more than 10 questions

    data_dict = {
        "data": [
            {"question1": questions[0]},
            {"question2": questions[1]},
            {"question3": questions[2]},
            {"question4": questions[3]},
            {"question5": questions[4]},
            {"question6": questions[5]},
            {"question7": questions[6]},
            {"question8": questions[7]},
            {"question9": questions[8]},
            {"question10": questions[9]},
        ]
    }

    json_output = json.dumps(data_dict, indent=4)
    print(json_output)
    return json_output

def advice(json_text, user_input):
    sample_feedback = {
        "data": [
            {"strength": ""},
            {"improvement": ""},
            {"suggested_actions": ""},
            {"brief_review": ""},
            {
  "suggested_courses": [
    {
      "name": "Course Name",
      "link": "Course Link"
    },
    {
      "name": "Course Name",
      "link": "Course Link"
    }
  ]
}
        ]
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert resume consultant providing feedback on resumes based on a job description {user_input} and CV in JSON format.
                {json_text}
                Follow these Instructions and Rules:
                Match & Analyze:
                    - Compare skills, experience, education, and certifications between CV and JD.
                    - Identify both strong matches and areas of weakness in the candidate's qualifications for the specific role.
                Feedback Generation:
                    - If there's a significant mismatch:
                        - Provide feedback with specific reasons for the mismatch across skills, experience, etc.
                        - Offer tailored improvement tips for relevant areas (e.g., acquiring certifications, highlighting relevant projects).
                        - Suggest relevant courses from Coursera and Udemy to improve weak areas.
                        - Include a brief overall summary of the candidate’s fit for the role.

                    - If there's a partial match:
                        - Highlight the candidate's strong matching qualifications.
                        - Recommend specific actions to strengthen weaker areas based on JD requirements (e.g., emphasize quantifiable achievements, tailor CV to specific role).
                Output:
                    - Generate feedback in JSON format with details like:
                        - Matching strengths 
                        - Areas for improvement with actionable suggestions

                Your answer should be in JSON format exactly matching the structure of {sample_feedback} without any extra formatting or quotes.
                """
            }
        ],
    )
    response_message = response.choices[0].message.content
    return response_message


def cover_letter(json_text, user_input):
    ########################################
    details = user_input
    print("################",details)
    struct = {
        "personal_detail": {
            "name": "<get data from (json_text cv)>",
            "email": "<get data from (json_text cv)>",
            "address": "<get data from (json_text cv)>",
        },
        "recipient_details": {
            "name": details["recipient_name"],
            "company_name": details["company_name"],
            "company_address": details["company_address"],
        },
        "job_description": details["job_description"],
    }
    ###########################################
    output = {
        "header": [
            {
                "name": "[replace by recipient_name]",
                "company_name": "[replace by company_name]",
                "company_address": "[replace by company_address]",
            }
        ],
        "greeting_sentence": "[replace by greeting_sentence]",
        "body": "[replace by body paragraphs]",
        "ending_lines": "[replace by ending lines]",
        "regards": "[replace by your sincerely and sender name ]",
    }
    ###########################################

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert cover letter builder. Your task is to match the skills, experience, and qualifications in a CV (provided as JSON text) with the requirements listed in a job description (provided as a structured JSON object). 

                Follow these Instructions:
                - Match Check: Carefully compare the CV {json_text} with the job description {struct}. 
                  Identify key skills, experiences, and qualifications required for the job. Check if these key elements are present in the CV.
                
                Output: When generating a cover letter, structure the response in the specified JSON format {output}. 
                Ensure the JSON response is properly formatted without extra characters or markdown (e.g., ```json).
                """
            }
        ],
    )
    response_message = response.choices[0].message.content
    return response_message
  # -Condition for Generating Cover Letter: If the key skills, experiences, and qualifications in the CV align with those in the job description, proceed to generate a cover letter. If the CV does not match the job description, respond with: "Sorry, your CV does not match the job description." 

def profile_building(json_text):
    # unethical = {"label":"UnEthical",
    #         "reason": "<express the reason to declare it as unethical.>"}
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": f"""
                you are a profile generator, and your job is to make a profile paragraph, while following the steps given below.


                    To create a profile, you will be given a json structured text {json_text} which is a text from the CV of a person.
                    Profile Generation Instructions:
                    - Generate a profile that emphasizes the candidate's qualifications and experiences.
                    - Highlight the candidate's strengths, achievements, and abilities.
                    - Ensure the profile is well-written, coherent, and professionally presented.
                    - Generate a maximum 100 word paragraph for a profile professionally accordingly. 
                    - Write the text in first person reference but do not mention the name.
                
                    Additional Notes:
                    - Provide specific examples or instances from the CV that demonstrate the candidate's proficiency in relevant areas.
                    - Consider the tone and language appropriate for a professional profile, ensuring clarity and effectiveness in communication.
                    - Remember that you have to follow each and every step provided above, and take your time to think before generating the profile,

 """,
            }
        ],
    )
    response_message = response.choices[0].message.content
    return response_message

def score_calculator(json_text, user_input):
    print(json_text)
    out_put = {"Eligibility_Score": "calculated_percentage_score"}
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": f"""you are a helpful eligibility score calculator, and you have to follow following the Instructions strictly. 
                - You have to calculate relative percentage that the given cv of a user given as {json_text},can be placed at the job having the description as {user_input},you have to return the output as {out_put}, 
                - To evaluate you have to think about the data provided in the cv, and the skills required for the specific job description, if they are of the same fields (then you have to examine them in more detail if they are of same sub feild then score should be some what greater than 80, else not more than 50 to 60).
                - Else if they are of totally different fields(then you should not score them more than 10 to 20 percent ), 
                - Again deeply analyse the relation between cv and job description do not assume or hallucinate,  before making decision.
                - At the end you only have to return answer as form of {out_put} always return the json in double quotes without the % sign, nothing else.""",
            }
        ],
    )

    response_message = response.choices[0].message.content
    return response_message


def is_cv(text):
    # Core CV keywords
    cv_keywords = ['experience', 'education', 'skills']
    
    # Join text segments if text is a list of strings
    if isinstance(text, list):
        text = ' '.join(text)
    
    # Convert to lowercase for case-insensitive comparison
    text_lower = text.lower()

    # Count the number of core keywords found
    keyword_count = 0
    for keyword in cv_keywords:
        if keyword in text_lower:
            keyword_count += 1

    # Consider the text as a CV if at least one keyword is found
    if keyword_count >= 1:
        return True
    
    return False

#Adding Fucntion to put the check on pdf file size
def get_file_size(file_path):
    # Check if file exists
    if os.path.exists(file_path):
        # Get file size in bytes
        file_size = os.path.getsize(file_path)
        # Convert bytes to kilobytes (optional)
        file_size_kb = file_size / 1024
        print(f"The siz of file {file_path} in KBs is: {file_size_kb}")
        if file_size_kb > 2048:
            print("X")
            return False
        else:
            print("Y")
            return True
    else:
        print("File not found.")
        return None

def convert_pdf_to_text(pdf_file_path, banned_words):
    # Check file size
    resultt = get_file_size(pdf_file_path)
    if resultt == False: #not get_file_size(pdf_file_path):
        print(f"The PDF file size exceeds the limit | Rejected: {pdf_file_path}")
        return pdf_file_path, False
    
    # Get the file extension
    _, file_extension = os.path.splitext(pdf_file_path)
    # Convert to lowercase for case-insensitive comparison
    file_extension = file_extension.lower()
    # Check if the file extension is either .pdf or .docx
    if file_extension == '.pdf':
        print(f"{pdf_file_path} is a PDF file.")
        # Extract text from PDF using pdfplumber
        with pdfplumber.open(pdf_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                break

    elif file_extension == '.docx':
        print(f"{pdf_file_path} is a Word file.")
        doc = docx.Document(pdf_file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        # return '\n'.join(text)
        print("This is the Text Extracted from Docx File ########", text)
    
    # Check if the extracted text indicates a CV
    if is_cv(text):
        # return pdf_file_path, True
        # Check for banned words
        for word in banned_words:
            if word.lower() in text.lower():
                print("Sorry, irrelevant content found.")
                return ("Prohibited Content Alter"), None
        # print("##########################9999999", text)
        return text, True
    else:
        return text, False



def JSON(user_input):
    details = """you have to make it structured as a dictionary format like as following, try to get all the insights of the cv and list them down, 
    Here is the corrected JSON with all single quotes replaced by double quotes:

    {
       'name' : 'details',
       'contact_number': 'details',
       'email': 'details',
       'linkedin': 'details',
       'address': 'details',       
       'profile' : 'profile paragraph'
       'education'   : 'details',
       'skills': 'details',
       'experience': 'details',
       'courses'  : 'details',
       'language'  : 'details'
       } 

    also if you found any other relevant information also list them as well."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": f"you are a helpful assistant, please provide a structured format of the following text {user_input} user provides you. In no way are you allowed to hallucinate or make up answers. {details}. Must follow the format I have Given Above and in single qoutes and do not output in doubble qoutes",
            }
        ],
    )
    response_message = response.choices[0].message.content
    print("##@@#@#@#@#@@#@#@#@#@#@#@#", response_message)
    return response_message


def CV_updation(json_text, user_input):
    output_struct = {
        "personal_info": [
            {"name": "<Get from cv data given as json_text>"},
            {"email": "<Get from cv data given as json_text>"},
            {"contact_number": "<Get from cv data given as json_text>"},
            {"job_title": "<get from user_input>"},
            {"linkedin": "<Get from cv data given as json_text>"},
        ],
        "profile": "<>",
        "education": [
            {"e1": "<Get from cv data given as json_text>"},
            {"e2": "<Get from cv data given as json_text>"},
            {"e3": "<Get from cv data given as json_text>"},
        ],
        "experience": [
            {"experience1": "<Get from cv data given as json_text>"},
            {"experience2": "<Get from cv data given as json_text>"},
            {"experience3": "<Get from cv data given as json_text if any exists>"},
        ],
        "skills": [
            {"s1": "<Get from cv data given as json_text>"},
            {"s2": "<Get from cv data given as json_text>"},
            {"s3": "<generate any other skill as per-requirement of job >"},
        ],
        "courses": [
            {"c1": "<Get from cv data given as json_text>"},
            {"c2": "<list done all courses as given in cv data given as json_text>"},
        ],
        "language": [
            {"L1": "<Get from cv data given as json_text>"},
            {"L2": "<Get from cv data given as json_text>"},
            {"L3": "<Get from cv data given as json_text if exists>"},
        ],
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": f"You are a resume updater, based on this existing resume data: {json_text} and then update it accordingly to the following job description: {user_input}. what you have to do is that make the CV with absolutely same structure as of {output_struct}, as the best fit with everything that is in the job description (for example the profile paragraph should be according to job description, the expertise , experience and other things should be according to job description ). you are allowed to be a bit creative to make new cv according to job description. output should be in the form of JSON,  provide each section of your response json in double quotes. ",
            }
        ],
    )
    response_message = response.choices[0].message.content
    return response_message


########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def create_cv_with_ai(json_text):
    contnt = """
    you are a CV creator, and your job is to make a best cv while analyzing the following details.
    Given JSON data is the information of the user that will be inserted into a CV, your task is to:
    create CV on the basis of following data, and the output should be in same structure as of input json.
    Identify  variables (in the provided json) that had no values or text, and try to fill them according to your experties, but not the empty ones.
    fill those to make a proper complete professional CV. however use the available information to come up with closely related things or things that might suit best. Make a complete CV and treat json variables and headings that needs to be filled. the output should be as same as input structure json. try to be a bit creative and fill the empty thing or variable accordingly.
    Do not add anything from yourself, 
    return the variables with value null  """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"{contnt},{json_text}"}],
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message
