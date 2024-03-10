from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from adrf.decorators import api_view
from .models import Service, Version
from .serializers import ServiceSerializer, VersionSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from adrf.decorators import api_view
from .models import Service, Version
from .serializers import ServiceSerializer, VersionSerializer
from rest_framework.response import Response
from django.db.models import Q

from asgiref.sync import sync_to_async


from asgiref.sync import sync_to_async

@api_view(['POST'])
@csrf_exempt
def register_service(request):
    if request.method == 'POST':
        service_name = request.data.get('service_name')
        service_url = request.data.get('service_url')

        existing_service = Service.objects.filter(
            Q(service_name=service_name) | Q(version__service_url=service_url)
        )

        if existing_service.exists():
            return Response(
                {'message': 'Service with the same name or service URL already exists'},
                status=409  # Use status code 409 (Conflict)
            )

        service = Service.objects.create(
            service_name=service_name,
            description=request.data.get('description')
        )

        Version.objects.create(
            service=service,
            version_number=request.data.get('version_number'),
            service_url=service_url
        )

        return Response({'message': 'Service registered successfully'}, status=201)

    return Response({'message': 'Invalid request method'}, status=400)



@api_view(['GET'])
def get_service_info(request, service_name):
    try:
        service = Service.objects.get(service_name=service_name)
    except Service.DoesNotExist:
        return Response({'error': 'Service does not exist'}, status=404)

    service_serializer = ServiceSerializer(instance=service)
    serialized_data = service_serializer.data
    return Response(serialized_data, status=200)


def get_services(request):
    services = Service.objects.all()
    service_data = []
    for service in services:
        versions = Version.objects.filter(service=service)
        version_data = []
        for version in versions:
            version_data.append({
                'version_number': version.version_number,
                'release_date': version.release_date,
                'service_url': version.service_url
            })
        service_data.append({
            'service_name': service.service_name,
            'status': service.status,
            'description': service.description,
            'start_date': service.start_date,
            'end_date': service.end_date,
            'versions': version_data
        })
    return JsonResponse(service_data, safe=False)

@api_view(['POST'])
@csrf_exempt
async def add_version(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service does not exist'}, status=404)

    if request.method == 'POST':
        version_data = request.data.copy()
        version_data['service'] = service_id
        version_serializer = VersionSerializer(data=version_data)
        if version_serializer.is_valid():
            version_serializer.save()
            return JsonResponse(version_serializer.data, status=201)
        return JsonResponse(version_serializer.errors, status=400)


@api_view(['PUT'])
@csrf_exempt
async def update_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service does not exist'}, status=404)

    if request.method == 'PUT':
        service_serializer = ServiceSerializer(service, data=request.data, partial=True)
        if service_serializer.is_valid():
            service_serializer.save()
            return JsonResponse(service_serializer.data, status=200)
        return JsonResponse(service_serializer.errors, status=400)
