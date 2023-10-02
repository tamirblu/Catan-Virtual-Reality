import tkinter as tk
from PIL import Image, ImageTk
import cv2
import random
import numpy as np


def read_resources_file(filename):
    resources = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(':')
            name = parts[0]
            vertex_strings = parts[1].strip('()').split('),(')
            float_vertices = []
            edges_strings = parts[2].strip('()').split('),(')
            for v in vertex_strings:
                coordinates = v.split(',')
                x, y, z = map(float, coordinates)
                float_vertices.append((x, y, z))
            float_edges = []
            for edge_list in edges_strings:
                x, y = edge_list.strip(')\n').split(',')
                float_edges.append((int(x), int(y)))
            resources[name] = (float_vertices, float_edges)
    return resources

def move_vertices(vertices, distance_x, distance_y):
    vertices2 = []
    # Loop over all vertices and move them to the new position with padding
    for i in range(len(vertices)):
        x = distance_x + vertices[i][0]
        y = distance_y + vertices[i][1]
        z = vertices[i][2]
        vertices2.append((x, y, z))
    return vertices2


def color_and_rand(file_name):
    color1 = (255, 179, 102)
    color2 = (0, 0, 0)
    color3 = (0, 0, 0)
    rand_val1 = 0.7
    rand_val2 = 0.7
    rand_val3 = 0.7
    if file_name == 'Tree':
        color1 = (102, 51, 0)
        color2 = (0, 0, 0)
        color3 = (0, 0, 0)
        rand_val1 = 0.6
    if file_name == 'Sheep':
        color1 = (1, 1, 1)
        color2 = (0, 102, 0)
        color3 = (160, 160, 160)
        rand_val1 = 0.9
    if file_name == 'Mortar':
        color1 = (255, 179, 102)
        color2 = (0, 0, 0)
        color3 = (0, 0, 0)
        rand_val1 = 0.9
    if file_name == 'Wheat':
        color1 = (204, 204, 0)
        color2 = (224, 224, 224)
        color3 = (0, 0, 0)
        rand_val1 = 0.5
    if file_name == 'Rock':
        color1 = (160, 160, 160)
        color2 = (0, 0, 0)
        color3 = (0, 0, 0)
        rand_val1 = 0.7
    return color1, color2, color3, rand_val1, rand_val2, rand_val3


def plot_world_points(file_name, resource, pad, pad_y, M_matrices, image_to_show):
    vertices2 = resource[0]
    edges = resource[1]
    thickness = 2
    image_with_cube = image_to_show

    color1, color2, color3, rand_val1, rand_val2, rand_val3 = color_and_rand(file_name)

    vertices = move_vertices(vertices2, pad_y, pad)

    homogeneous_points = [M_matrices @ np.transpose(np.concatenate(([vertice], [[1]]), axis=1)) for vertice in vertices]
    xy_projection_dot = [homogeneous_point[0:2, :] / homogeneous_point[2, 0] for homogeneous_point in
                         homogeneous_points]

    if file_name == 'Mortar' or file_name == 'Wheat' or file_name == 'Rock' or file_name == 'Tree':
        for edge in edges:
            if edge[0] - 1 < len(xy_projection_dot) - 1 and edge[1] - 1 < len(xy_projection_dot) - 1:
                x = [xy_projection_dot[edge[0] - 1][0], xy_projection_dot[edge[1] - 1][0]]
                y = [xy_projection_dot[edge[0] - 1][1], xy_projection_dot[edge[1] - 1][1]]
                random_float = random.random()
                if random_float < rand_val1:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), color1,
                                               thickness)
                else:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), color2,
                                               thickness)
    if file_name == 'Sheep':
        for edge in edges:
            if edge[0] - 1 < len(xy_projection_dot) - 1 and edge[1] - 1 < len(xy_projection_dot) - 1:
                x = [xy_projection_dot[edge[0] - 1][0], xy_projection_dot[edge[1] - 1][0]]
                y = [xy_projection_dot[edge[0] - 1][1], xy_projection_dot[edge[1] - 1][1]]
                z = [vertices[edge[0] - 1][2], vertices[edge[1] - 1][2]]
                x2 = [vertices[edge[0] - 1][0], vertices[edge[1] - 1][0]]
                random_float = random.random()
                if z[0] > 1.5:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), color1,
                                               thickness)
                elif z[0] < 0.5:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])),
                                               (250, 250, 250), thickness)
                elif random_float < rand_val1:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), color2,
                                               thickness)
                else:
                    image_with_cube = cv2.line(image_with_cube, (int(x[0]), int(y[0])), (int(x[1]), int(y[1])), color3,
                                               thickness)



def func2(user1, user2, image_read, image_to_show):
    copy = np.copy(image_to_show)
    resources = read_resources_file('ICBV231-1-resources.txt')
    M_matrices = np.loadtxt('ICBV231-1-Matrice.txt', delimiter=",")

    # player 1:
    Tree_num1 = user1[0]
    Sheep_num1 = user1[1]
    Wheat_num1 = user1[2]
    Rock_num1 = user1[3]
    Mortar_num1 = user1[4]
    player1 = {'Sheep': Sheep_num1, 'Rock': Rock_num1, 'Wheat': Wheat_num1, 'Mortar': Mortar_num1, 'Tree': Tree_num1}

    # player 2:
    Tree_num2 = user2[0]
    Sheep_num2 = user2[1]
    Wheat_num2 = user2[2]
    Rock_num2 = user2[3]
    Mortar_num2 = user2[4]
    player2 = {'Sheep': Sheep_num2, 'Rock': Rock_num2, 'Wheat': Wheat_num2, 'Mortar': Mortar_num2, 'Tree': Tree_num2}

    players = [player1, player2]

    pad = -7.5
    pad_y = -23
    # plot
    print("user1:")
    print(user1)
    print("user2:")
    print(user2)
    for j in range(len(players)):
        if j == 1:
            pad = -8
            pad_y = 24
        if j == 0:
            pad = -7
            pad_y = -23
        for file_name, resource in resources.items():
            for key, value in players[j].items():
                if j == 1:
                    pad_y = 24
                if j == 0:
                    pad_y = -23
                if key == file_name:
                    for x in range(players[j][key]):
                        plot_world_points(file_name, resource, pad, pad_y, M_matrices, copy)
                        if j == 1:
                            pad_y -= 4.5
                        if j == 0:
                            pad_y += 4
                        if x == players[j][key] - 1:
                            pad += 3.8

    return copy


# Function that generates an image based on the input parameters
def generate_image(user1, user2):
    # Your image generation code goes here
    image_read = cv2.imread('ICBV231-1-katan_image.jpeg')
    image_to_show = cv2.cvtColor(image_read, cv2.COLOR_BGR2RGB)
    copy_image_to_show = np.copy(func2(user1, user2, image_read, image_to_show))

    return copy_image_to_show

# Function that generates the output image on the GUI
def generate_output():
    # Get input values from the user
    user1 = [int(entry1[c1].get()) for c1 in range(5)]
    user2 = [int(entry2[c2].get()) for c2 in range(5)]
    # Generate the output image based on the input values
    image = generate_image(user1, user2)
    show_image(image)


def generate_random():
    user1 = [random.randint(0, 4) for i in range(5)]
    user2 = [random.randint(0, 4) for i in range(5)]
    image = generate_image(user1, user2)
    show_image(image)

def show_image(image):
    # Resize the image to 500x500 pixels
    img = Image.fromarray(image)
    img = img.resize((380, 380))

    # Convert the output image to a Tkinter PhotoImage and display it on the GUI
    photo = ImageTk.PhotoImage(img)
    output_label.config(image=photo)
    output_label.image = photo

def resource_int_toStr(i):
    i = i+1
    if i == 1:
        return "Wood..."
    elif i == 2:
        return "Sheep..."
    elif i == 3:
        return "Wheat..."
    elif i == 4:
        return "Iron..."
    elif i == 5:
        return "Clay..."
    else:
        print("Error - no such Resource")


# Create the GUI window and widgets
root = tk.Tk()
root.title("CATAN Resources Projection - Final Project")

# Create the top frame for the static image
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="both")
label_top = tk.Label(top_frame)
label_top.pack()

# Load the top image
top_image = Image.open("ICBV231-1-res.jpg")
top_photo = ImageTk.PhotoImage(top_image)

# Display the top image on the GUI
top_label = tk.Label(top_frame, image=top_photo)
top_label.image = top_photo
top_label.pack()

# Create the bottom frame for the generated image
output_frame = tk.Frame(root)
output_frame.pack(side="bottom", fill="both")

label_output = tk.Label(output_frame) #, text="Generated Image"
label_output.pack()

output_label = tk.Label(output_frame)
output_label.pack()

# Create the frame for the input fields for User 1
user1_frame = tk.Frame(root)
user1_frame.pack(side="left")

label_user1 = tk.Label(user1_frame, text="User 1")
label_user1.pack()

entry1 = [tk.Entry(user1_frame) for _ in range(5)]
for i in range(5):
    entry1[i].insert(0, str(resource_int_toStr(i)))
    entry1[i].pack()

# Create the frame for the input fields for User 2
user2_frame = tk.Frame(root)
user2_frame.pack(side="right")

label_user2 = tk.Label(user2_frame, text="User 2")
label_user2.pack()

entry2 = [tk.Entry(user2_frame) for _ in range(5)]
for i in range(5):
    entry2[i].insert(0, str(resource_int_toStr(i)))
    entry2[i].pack()

# Create the Generate button to generate the output image
generate_button = tk.Button(root, text="Generate Image", command=generate_output)
generate_button.pack()

randomVal_button = tk.Button(root, text="Random Values", command=generate_random)
randomVal_button.pack()

# Create the Exit button to close the window
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()

