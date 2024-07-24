import unittest
from app import app
from io import BytesIO


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
###################################################################################################################
    def test_cv_upload(self):
        with open('coverletter.pdf', 'rb') as f:
            pdf_content = f.read()

        response = self.app.post('/cv_upload', data={
            'session': '98791234',
            'cv': (BytesIO(pdf_content), 'test_cv.pdf')
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'CV uploaded')
##################################################################################################################
    def test_profile_building_success(self):
            def mock_get_cv_data(session):
                return {"cv_data": "mocked_cv_data"}

            app.get_cv_data = mock_get_cv_data

            # Making a POST request to the endpoint with required data
            response = self.app.post('/profile_building', data={
                'session': '98791234',
                'variable': 'test_variable'
            })
            # Asserting that the response status code is 200
            self.assertEqual(response.status_code, 200)
            # Asserting that the response message is as expected
###################################################################################################################

    def test_profile_building_missing_variable(self):
        # Making a POST request to the endpoint without variable
        response = self.app.post('/profile_building', data={
            'session': '98791234',
        })

        # Asserting that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Asserting that the response message is as expected
        self.assertEqual(response.json['message'], 'variable is missing in the request.')
###################################################################################################################

    def test_cover_letter_success(self):
        # Mocking the data retrieval function get_cv_data
        def mock_get_cv_data(session):
            return {"cv_data": "mocked_cv_data"}

        app.get_cv_data = mock_get_cv_data

        # Making a POST request to the endpoint with required data
        response = self.app.post('/cover_letter', data={
            'session': '98791234',
            'r_name': 'Recipient Name',
            'company_name': 'Company Name',
            'company_address': 'Company Address',
            'job_description': 'Job Description'
        })

        # Asserting that the response status code is 200
        self.assertEqual(response.status_code, 200)
###################################################################################################################


    def test_cover_letter_missing_data(self):
        # Making a POST request to the endpoint without providing all required data
        response = self.app.post('/cover_letter', data={
            'session': '98791234',
            'r_name': 'Recipient Name',
            'company_name': 'Company Name',
            # Missing company_address and job_description
        })

        # Asserting that the response status code is 400
        self.assertEqual(response.status_code, 400)

###################################################################################################################

def test_advice_feedback_success(self):
        # Mocking the data retrieval function get_cv_data
        def mock_get_cv_data(session):
            return {"cv_data": "mocked_cv_data"}

        app.get_cv_data = mock_get_cv_data

        # Making a POST request to the endpoint with required data
        response = self.app.post('/advice_feedback', data={
            'session': '98791234',
            'job_designation': 'Test Job Designation'
        })

        # Asserting that the response status code is 200
        self.assertEqual(response.status_code, 200)
###################################################################################################################

def test_advice_feedback_missing_description(self):
    # Making a POST request to the endpoint without providing job_designation
    response = self.app.post('/advice_feedback', data={
        'session': '98791234',
        # Missing job_designation
    })

    # Asserting that the response status code is 400
    self.assertEqual(response.status_code, 400)

###################################################################################################################

def test_interview_question_success(self):
        # Making a POST request to the endpoint with required data
        response = self.app.post('/interview_questions', data={
            'session': '98791234',
            'job_description': 'Test Job Description'
        })

        # Asserting that the response status code is 200
        self.assertEqual(response.status_code, 200)


###################################################################################################################

def test_interview_question_missing_description(self):
    # Making a POST request to the endpoint without providing job_description
    response = self.app.post('/interview_questions', data={
        'session': '98791234',
        # Missing job_description
    })

    # Asserting that the response status code is 400
    self.assertEqual(response.status_code, 400)

###################################################################################################################

def test_cv_upd_success(self):
        # Mocking the data retrieval function get_cv_data
        def mock_get_cv_data(session):
            return {"cv_data": "mocked_cv_data"}

        app.get_cv_data = mock_get_cv_data

        # Making a POST request to the endpoint with required data
        response = self.app.post('/CV_updation', data={
            'session': '98791234',
            'job_designation': 'Test Job Designation'
        })

        # Asserting that the response status code is 200
        self.assertEqual(response.status_code, 200)


###################################################################################################################

def test_cv_upd_missing_description(self):
    # Making a POST request to the endpoint without providing job_designation
    response = self.app.post('/CV_updation', data={
        'session': '98791234',
        # Missing job_designation
    })

    # Asserting that the response status code is 400
    self.assertEqual(response.status_code, 400)

###################################################################################################################

def test_cv_create_success(self):
        # Mocking the request JSON data
        mock_request_data = {
            "key1": "value1",
            "key2": "value2",
            # Add more fields as needed
        }

        # Making a POST request to the endpoint with mock request data
        response = self.app.post('/create_CV', json=mock_request_data)

        # Asserting that the response status code is 200
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()

