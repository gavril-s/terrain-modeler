from scipy.spatial import Delaunay
import csv
import numpy as np
import os
import plotly.graph_objects as go
import uuid
import elevation_fetcher


def generate(output_dir, top_left, bottom_right, lat_points, lon_points, show_points, api):
    elevations = elevation_fetcher.fetch_rectangle(top_left, bottom_right, lat_points, lon_points, api)
    id = generate_html(output_dir, elevations, show_points)
    generate_csv(output_dir, id, elevations)
    return id


def generate_html(output_dir, data, show_points):
    x = np.array([point[0] for point in data])
    y = np.array([point[1] for point in data])
    z = np.array([point[2] for point in data])

    tri = Delaunay(np.column_stack((x, y, z)))
    triangulation_points = tri.points[tri.simplices]

    x_tri = triangulation_points[:, :, 0].flatten()
    y_tri = triangulation_points[:, :, 1].flatten()
    z_tri = triangulation_points[:, :, 2].flatten()

    surface = go.Mesh3d(
        x=x_tri,
        y=y_tri,
        z=z_tri,
        intensity=z_tri,
        color="lightblue",
        opacity=0.95 if show_points else 1,
        showscale=True,
        flatshading=True,
        lighting=dict(ambient=0.6, diffuse=0.4, specular=0.3, roughness=0.5) 
    )

    plots = [surface]
    if show_points:
        points = go.Scatter3d(x=x, y=y, z=z, mode="markers", marker=dict(size=4, color="black"))
        plots.append(points)
    fig = go.Figure(data=plots)
    fig.update_layout(scene=dict(
        xaxis_title="X", yaxis_title="Y", zaxis_title="Z" # lon, lat, height
    ))  

    id = uuid.uuid4()
    filename = f"{id}.html"
    fig.write_html(os.path.join(output_dir, "models", filename))
    return id


def generate_csv(output_dir, id, data):
    output_file = os.path.join(output_dir, "csv", f"{id}.csv")
    with open(output_file, "w", newline="") as out:
        writer = csv.writer(out)
        for row in data:
            writer.writerow(row)
