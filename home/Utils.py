import cv2
import numpy as np
import networkx as nx
import threading
import tkinter as tk


def insert_nodes(image_path, node_coordinates, node_names=None):
    # Load image
    img = cv2.imread(image_path)

    # Define node color (here, using red)
    node_color = (0, 0, 255)

    # Draw nodes on image
    for i, (x, y) in enumerate(node_coordinates):
        # Draw circle for node
        cv2.circle(img, (x, y), radius=3, color=node_color, thickness=-1)  # filled circle

        # Add node name as text
        if node_names:
            cv2.putText(img, node_names[i], (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, node_color, 1)

    return img


def find_shortest_path(node_coordinates, start_node_name, end_node_name):
    # Create a graph
    node_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','X','Y','Z','A1','B3','C1','D2','E1','F1'] # Example node names (optional)

    G = nx.Graph()
    for i, (x, y) in enumerate(node_coordinates):
        G.add_node(i, pos=(x, y))  # Add node with position

    # Add edges based on proximity
    for i in range(len(node_coordinates)):
        for j in range(i + 1, len(node_coordinates)):
            dist = np.linalg.norm(np.array(node_coordinates[i]) - np.array(node_coordinates[j]))
            if dist < 130:  # Adjust the threshold as needed
                G.add_edge(i, j)

    # Find indices of start and end nodes
    start_node_index = node_names.index(start_node_name)
    end_node_index = node_names.index(end_node_name)

    # Find shortest path using Dijkstra's algorithm
    shortest_path_indices = nx.shortest_path(G, source=start_node_index, target=end_node_index)

    return shortest_path_indices


def generate_directions(shortest_path_indices, node_coordinates, node_names):
    directions = []
    for i in range(len(shortest_path_indices) - 1):
        start_node_name = node_names[shortest_path_indices[i]]
        end_node_name = node_names[shortest_path_indices[i + 1]]
        start_coord = node_coordinates[shortest_path_indices[i]]
        end_coord = node_coordinates[shortest_path_indices[i + 1]]
        direction = get_direction(start_coord, end_coord)
        directions.append(f"Go {direction} from {start_node_name} to {end_node_name}")
    return directions


# def speak_direction(direction):
#     engine = pyttsx3.init()
#     engine.say(direction)
#     engine.runAndWait()


def get_direction(start_coord, end_coord):
    dx = end_coord[0] - start_coord[0]
    dy = end_coord[1] - start_coord[1]
    angle = np.arctan2(dy, dx) * 180 / np.pi
    if angle < 0:
        angle += 360
    if 45 <= angle < 135:
        return "upwards"
    elif 135 <= angle < 225:
        return "leftwards"
    elif 225 <= angle < 315:
        return "forward"
    else:
        return "rightwards"


def draw_path(img, shortest_path_indices, node_coordinates):
    # Draw shortest path as dotted line
    for i in range(len(shortest_path_indices) - 1):
        start_coord = node_coordinates[shortest_path_indices[i]]
        end_coord = node_coordinates[shortest_path_indices[i + 1]]
        cv2.line(img, start_coord, end_coord, (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
    return img


def display_image_with_path(img, window_name):
    img_with_path = img.copy()
    cv2.imshow(window_name, img_with_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def on_button_click(directions):
#     for direction in directions:
#         speak_direction(direction)

if __name__ == "__main__":

    # Example usage
    image_path = r'static\assets\image.jpeg'  # Path to input image
    node_coordinates = [(53, 259),(53, 306),(64, 347),(165, 347),(206, 347),(248, 326),(306, 327),(156, 220),
    (199, 225),(370, 209),(391, 184),(415, 211),(513, 325),(559, 324),(629, 345),(595, 345),
    (737, 344),(754, 314),(753, 254),(628, 225),(589, 226),(158, 271),(251, 271),(330, 273),
    (387, 248),(425, 275),(527, 274),(589, 268),(670, 281),(733, 278)]  # Example node coordinates
    node_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','X','Y','Z','A1','B3','C1','D2','E1','F1'] # Example node names (optional)

    img = insert_nodes(image_path, node_coordinates, node_names)

    # Input from user for start and end nodes
    start_node_name = input('Enter the name of the start node: ')
    end_node_name = input('Enter the name of the end node: ')

    # Find shortest path
    shortest_path_indices = find_shortest_path(node_coordinates, start_node_name, end_node_name)

    # Generate directions
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)

    # Print directions
    for direction in directions:
        print(direction)

    # Create a button for voice output
    root = tk.Tk()
    # button = tk.Button(root, text="Start Voice Output", command=lambda: on_button_click(directions))
    # button.pack()

    # Display image with nodes and shortest path
    image_thread = threading.Thread(target=display_image_with_path, args=(
    draw_path(img, shortest_path_indices, node_coordinates), 'Image with Nodes and Shortest Path'))
    image_thread.start()

    root.mainloop()