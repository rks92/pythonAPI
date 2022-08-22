from rest_framework import status
import json
from rest_framework.test import APITestCase
from .factories import PatientFactory


# Required to enable SkipTest
# import unittest


class APITest(APITestCase):
    def test_get_patient(self):
        patient_mocks = PatientFactory.create_batch(4)
        response = self.client.get('/patient/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()), 4)

    def test_create_patient(self):
        # Create assertable responses
        error_response = self.client.post(
            '/patient/',
            data=dict(email="", name=""),
            format='json'
        )
        valid_response = self.client.post(
            '/patient/',
            data=dict(email="sally@floatfi.com", name="Sally Jones"),
            format='json'
        )
        self.assertEquals(error_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(valid_response.status_code, status.HTTP_201_CREATED)

    def test_ehr_webhook(self):
        all_inserted = self.client.post(
            '/ehr_webhook/',
            data=[
                dict(email="valid_one@test.com", name="Valid User One"),
                dict(email="valid_two@test.com", name="Valid User Two"),
            ],
            format='json'
        )

        self.assertEquals(all_inserted.status_code, status.HTTP_201_CREATED)

        response_str = all_inserted.content.decode('utf-8')
        response = json.loads(response_str)
        self.assertEquals(len(response['succeeded']), 2)
        self.assertEquals(len(response['failed']), 0)

        one_failed = self.client.post(
            '/ehr_webhook/',
            data=[
                dict(email="", name=""),
                dict(email="valid_three@test.com", name="Valid User Three"),
            ],
            format='json'
        )
        self.assertEquals(one_failed.status_code, status.HTTP_201_CREATED)

        response_str = one_failed.content.decode('utf-8')
        response = json.loads(response_str)
        self.assertEquals(len(response['succeeded']), 1)
        self.assertEquals(len(response['failed']), 1)

        duplicates = self.client.post(
            '/ehr_webhook/',
            data=[
                dict(email="valid_four@test.com", name="Valid User Four"),
                dict(email="valid_four@test.com", name="Valid User Four"),
            ],
            format='json'
        )
        self.assertEquals(duplicates.status_code, status.HTTP_201_CREATED)

        response_str = duplicates.content.decode('utf-8')
        response = json.loads(response_str)
        self.assertEquals(len(response['succeeded']), 1)
        self.assertEquals(len(response['failed']), 1)
