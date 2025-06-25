import vtk
import numpy as np

# === CONFIG ===
filename = "Isabel_2D.vti"  # <-- replace with your actual VTK XML image data file
cell_id = 0                  # <-- can be changed to get info about any other cell
# =============

# Load the dataset
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(filename)
reader.Update()
data = reader.GetOutput()

# Number of cells and points
num_cells = data.GetNumberOfCells()
num_points = data.GetNumberOfPoints()
dims = data.GetDimensions()

# Get Pressure array
pressure_array = data.GetPointData().GetArray("Pressure")

# Compute pressure range and average
pressure_range = pressure_array.GetRange()
pressure_values = [pressure_array.GetValue(i) for i in range(pressure_array.GetNumberOfTuples())]
average_pressure = sum(pressure_values) / len(pressure_values)

# Extract the specified cell
cell = data.GetCell(cell_id)
point_ids = [cell.GetPointId(i) for i in range(cell.GetNumberOfPoints())]

# Get coordinates of vertices
points = data.GetPoints()
coords = [points.GetPoint(pid) for pid in point_ids]

# Compute cell center
center = np.mean(coords, axis=0)

# Get pressure values at each vertex
vertex_pressures = [pressure_array.GetValue(pid) for pid in point_ids]
center_avg_pressure = sum(vertex_pressures) / len(vertex_pressures)

# === PRINT RESULTS ===
print(f"Number of cells: {num_cells}")
print(f"Dataset dimensions: {dims}")
print(f"Number of points: {num_points}")
print(f"Pressure range: {pressure_range}")
print(f"Average pressure: {average_pressure:.4f}")

print(f"\nCell ID = {cell_id}")
print("Corner vertex indices:", point_ids)
print("Corner vertex coordinates:")
for i, coord in enumerate(coords):
    print(f"  Vertex {i}: {coord}")
print(f"Cell center: {tuple(center)}")
print("Pressure at vertices:", vertex_pressures)
print(f"Mean pressure at cell center: {center_avg_pressure:.4f}")
