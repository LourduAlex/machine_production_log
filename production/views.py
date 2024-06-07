from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import AuthenticationFailed
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer

class RegisterView(APIView):
    def post(self, request, format=None):

        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            response_data = {
                'success': True,
                'message': "Account Created Successfully",
                'Id': instance.id,
                'machine_name': instance.machine_name,
                'machine_serial_no': instance.machine_serial_no,
                'time': instance.time
            }
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        machine_name = request.data.get('machine_name')
        machine_serial_no = request.data.get('machine_serial_no')

        machine_exists = Machine.objects.filter(machine_name=machine_name, machine_serial_no=machine_serial_no).first()

        if machine_exists is None:
            raise AuthenticationFailed({'success': 'false', 'message': 'Login Failed!'})
        

        Response.data = {
        'success': 'true',
        'message': 'login successfully ',
        'userId': machine_exists.id,
        'machine_name': machine_exists.machine_name
         }

        return Response
    
class CreateEditProductionLogView(APIView):

    def post(self, request, pk=None):
        if pk:
            try:
                productionlog_instance = ProductionLog.objects.get(pk=pk)
            except ProductionLog.DoesNotExist:
                return Response({"error": "ProductionLog not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductionLogSerializer(productionlog_instance, data=request.data)
            message_success = "Your ProductionLog has been successfully edited"
            message_failure = "Your ProductionLog cannot be edited"
        else:
            serializer = ProductionLogSerializer(data=request.data)
            message_success = "ProductionLog has been successfully created"
            message_failure = "ProductionLog failed to create"

        if serializer.is_valid():
            production_log = serializer.save()

            # OEE is automatically calculated in the model's save method
            production_log.save()

            return Response({
                'success': True,
                'message': message_success,
                'serializer': ProductionLogSerializer(production_log).data
            })
        else:
            return Response({
                'success': False,
                'message': message_failure,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            

class DeleteProductionLogView(APIView):
    def delete(self, request, id):
        try:
            video_instance = ProductionLog.objects.get(id=id)
            ProductionLog.delete()
            return Response({
            'success': True,
            'message': "ProductionLog Deleted successfully"})
        except ProductionLog.DoesNotExist:
            return Response({"error": "ProductionLog not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ProductionLogListView(ListAPIView):
    serializer_class = ProductionLog

    def list(self, request):
        id = self.request.query_params.get('id')

        if not id:
            return Response({"success": False, "message": "id is required"})


        machinelist = ProductionLog.objects.filter(id=id)
        message = "Video List retrieved successfully from a particular vendor."

        serialized_data = self.serializer_class(machinelist, many=True).data     

        status_code = status.HTTP_200_OK
        return Response(serialized_data, status=status_code)
    
