from django.shortcuts import render
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
import pandas as pd
from rest_framework import status
from .utils import *
from .models import Device
from .serializers import DeviceSerializer
import os
import csv
from rest_framework.pagination import PageNumberPagination
import joblib
from django.forms.models import model_to_dict

from price_classification.config import *

class DevicePagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100

@api_view(['GET'])
def retrieve_devices(request):
    try:
        print("request  :   ",request)
        paginator = DevicePagination()

        # get all devices
        devices = Device.objects.all()
        result_page = paginator.paginate_queryset(devices, request)
        serializer = DeviceSerializer(result_page, many=True)
        
        # get the page number of the current page
        current_page_number = paginator.page.number
        print("paginator.page.limit :   ", )

        
        # getting page size
        limit = request.query_params.get('limit', None)
        if limit:
            paginator.page_size = int(limit)
        else:
            paginator.page_size = 10

        return Response(
            {
                "page no.": current_page_number,
                "limit": paginator.page_size,
                "data": serializer.data
            }
        )
    except Exception as e:
        print("Error message    :   ",e)

@api_view(['GET'])
def fetch_device(request, device_id):
    try:
        device = Device.objects.get(id=device_id)
        serializer = DeviceSerializer(device, many=False)
        return Response({"device": serializer.data})
    except Exception as e:
        return f"Error message    :   {e}"

@api_view(['POST'])
def add_device(request):
    loaded_model = get_loaded_model()

    # Convert request data to a DataFrame
    # Transpose used to switch all rows to columns
    df = pd.DataFrame(request.data).transpose()
    df = get_best_columns(df)

    # predicting the price_range value by using trained model
    prediction = loaded_model.predict(df.values)
    # adding predicted price_range value in data
    request.data["data"]["price_range"] = int(prediction[0])

    serializer = DeviceSerializer(data=request.data["data"])

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def bulk_add_device(request):
    # get the path of current directly on which server are running
    current_dir = os.getcwd()

    # You can also add another csv file name here if you want to add the records in database
    csv_file_path = os.path.join(current_dir, TEST_CSV_FILE)
    if os.path.exists(csv_file_path):
        print("The CSV file exists in the current directory.")
    else:
        print("please add csv file to this")

    try:
        # read csv file 
        df = pd.read_csv(csv_file_path)
        # it will handle missing values like nan value
        # it uses KNNImputer
        df = handling_missing_values(df)

        # remove df id column
        if 'id' in df.columns:
            df.drop(columns=['id'], inplace=True)
        
        devices = []
        for index, row in df.iterrows():
            device_data = row.to_dict()  # Convert the row to a dictionary
            devices.append(Device(**device_data))
        # it will append all records at once
        Device.objects.bulk_create(devices)
        return Response({'message': 'Devices created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def predict_by_id(request, device_id):
    device = {}
    loaded_model = get_loaded_model()
    device_rec = Device.objects.get(id=device_id)
    device["data"] =  model_to_dict(device_rec)
    price_range = None
    try:
        price_range = device["data"]["price_range"]
    except:
        print("price field not present")
        
    print("device :  ", device)
    df = pd.DataFrame(device).transpose()
    df = get_best_columns(df)

    # predicting the price_range value by using trained model
    prediction = int(loaded_model.predict(df.values)[0])

    # adding predicted price_range value in data
    if prediction == price_range:
        msg = "Predicted Price Range Match"
    elif price_range == None:
        msg = "Price Column not present"
    else:
        msg = "Predicted Price Range Not Match"
        params = {"price_range":prediction}
        serializer = DeviceSerializer(device_rec, data=params, partial=True)
        if serializer.is_valid():
            serializer.save()
    
    return Response({"message   ":msg})

