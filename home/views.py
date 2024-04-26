from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import networkx as nx
from . Utils import insert_nodes, find_shortest_path, generate_directions,draw_path
from . models import *
from django.core.files.base import ContentFile
import base64



# Create your views here.
def home(request):
    return render(request, 'index.html')

import os
from django.conf import settings

def get_route(request):
    # Your existing code to generate image and directions
    image_path = r'static\assets\image.jpeg'  
    node_coordinates = [(53, 259),(53, 306),(64, 347),(165, 347),(206, 347),(248, 326),(306, 327),(156, 220),
    (199, 225),(370, 209),(391, 184),(415, 211),(513, 325),(559, 324),(629, 345),(595, 345),
    (737, 344),(754, 314),(753, 254),(628, 225),(589, 226),(158, 271),(251, 271),(330, 273),
    (387, 248),(425, 275),(527, 274),(589, 268),(670, 281),(733, 278)]  
    node_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','X','Y','Z','A1','B3','C1','D2','E1','F1']

    img = insert_nodes(image_path, node_coordinates, node_names)

    # Your existing code to find shortest path and generate directions
    start_node_name = request.GET.get('start_node_name')
    end_node_name = request.GET.get('end_node_name')
    print(start_node_name)
    print(end_node_name)
    shortest_path_indices = find_shortest_path(node_coordinates, str(start_node_name), str(end_node_name))
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)

    # Draw the path on the image
    draw_path(img, shortest_path_indices, node_coordinates)

    # Serialize the image data
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Save the image data to the static files directory
    image_filename = f'navigation_image_{start_node_name}_{end_node_name}.jpg'  # Unique filename
    image_path = os.path.join(r"static", 'navigation_images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Print directions
    for direction in directions:
        print(direction)
    response_data = {
        "directions": directions,
        "image_filename": image_filename  # Include the image filename in the response
    }

    # Return JSON response
    return JsonResponse(response_data)