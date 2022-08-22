from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


"""Just Testing"""


# class PatientViewSetTwo(viewsets.ModelViewSet):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer


@api_view(['POST'])
def bulk_insert(request):
    """
    Insert all records sent by request
    """
    print(request.data)
    succeeded = []
    failed = []
    for patient in request.data:
        """ These should be set to output at debug level in a real application"""
        try:
            print(f'Attempting to insert: {patient}')
            new_patient = PatientSerializer(None, patient)
            new_patient.is_valid(raise_exception=True)
            new_patient.save()
            print(f'Inserted {patient} successfully!')
            succeeded.append(patient)
        except Exception as e:
            print(e)
            failed.append({'patient': patient, 'reason': e.__dict__})

    return Response({'succeeded': succeeded, 'failed': failed}, status=status.HTTP_201_CREATED)
