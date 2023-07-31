from gl import Renderer, V2, color

width = 1024
height = 1024

rend = Renderer(width, height)

# Define the vertices of the first polygon (previous polygon)
polygon1_vertices = [
    (165, 380),
    (185, 360),
    (180, 330),
    (207, 345),
    (233, 330),
    (230, 360),
    (250, 380),
    (220, 385),
    (205, 410),
    (193, 383)
]

# Convert the first polygon vertices to V2 objects and draw the polygon with the desired color
polygon1_vertices_v2 = [V2(v[0], v[1]) for v in polygon1_vertices]
rend.glPolygon(polygon1_vertices_v2, color(1, 0, 0))  # Use red color (1, 0, 0)


# Define the vertices of the third polygon
polygon3_vertices = [
    (413, 177),
    (448, 159),
    (502, 88),
    (553, 53),
    (535, 36),
    (676, 37),
    (660, 52),
    (750, 145),
    (761, 179),
    (672, 192),
    (659, 214),
    (615, 214),
    (632, 230),
    (580, 230),
    (597, 215),
    (552, 214),
    (517, 144),
    (466, 180)
]

# Convert the third polygon vertices to V2 objects and draw the polygon with the desired color
polygon3_vertices_v2 = [V2(v[0], v[1]) for v in polygon3_vertices]
rend.glPolygon(polygon3_vertices_v2, color(0, 0, 1))  # Use blue color (0, 1, 0)

# Render the scene (including all three polygons)
rend.glRender()



# Define the vertices of the second polygon (diamond)
polygon2_vertices = [
    (682, 175),
    (708, 120),
    (735, 148),
    (739, 170)
]

# Convert the second polygon vertices to V2 objects and draw the polygon with the desired color
polygon2_vertices_v2 = [V2(v[0], v[1]) for v in polygon2_vertices]
rend.glPolygon(polygon2_vertices_v2, color(0, 0, 0))  # Use black color (0, 0, 1)


# Save the result to a file
rend.glFinish("output.bmp")