import vtk
import argparse

def extract_isocontour(input_file, output_file, isovalue):
    # Read the input VTKImageData
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    image_data = reader.GetOutput()
    dims = image_data.GetDimensions()
    spacing = image_data.GetSpacing()
    origin = image_data.GetOrigin()
    
    # Create polydata to store the contour
    poly_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    
    # Iterate through each cell in the 2D grid
    for j in range(dims[1] - 1):
        for i in range(dims[0] - 1):
            # Get the 4 vertices of the cell
            cell_values = []
            cell_points = []
            for y in [j, j+1]:
                for x in [i, i+1]:
                    val = image_data.GetScalarComponentAsDouble(x, y, 25, 0)
                    cell_values.append(val)
                    # Calculate actual coordinates
                    px = origin[0] + x * spacing[0]
                    py = origin[1] + y * spacing[1]
                    cell_points.append((px, py, 0))
            
            # Find edge intersections
            intersections = []
            
            # Check all 4 edges in counterclockwise order
            edges = [
                (0, 1),  # Bottom edge
                (1, 3),  # Right edge
                (2, 3),  # Top edge
                (0, 2)   # Left edge
            ]
            
            for edge in edges:
                v0, v1 = edge
                val0, val1 = cell_values[v0], cell_values[v1]
                
                # Check for crossing
                if (val0 < isovalue) != (val1 < isovalue):
                    t = (isovalue - val0) / (val1 - val0)
                    p0 = cell_points[v0]
                    p1 = cell_points[v1]
                    # Linear interpolation
                    x = p0[0] + t * (p1[0] - p0[0])
                    y = p0[1] + t * (p1[1] - p0[1])
                    intersections.append((x, y, 0))
            
            # Add line segment if we have exactly 2 intersections
            if len(intersections) == 2:
                pid1 = points.InsertNextPoint(intersections[0])
                pid2 = points.InsertNextPoint(intersections[1])
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, pid1)
                line.GetPointIds().SetId(1, pid2)
                lines.InsertNextCell(line)
    
    # Set up and write the output file
    poly_data.SetPoints(points)
    poly_data.SetLines(lines)
    
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(poly_data)
    writer.Write()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract 2D isocontour from VTKImageData')
    parser.add_argument('input', help='Input VTKImageData file (.vti)')
    parser.add_argument('output', help='Output VTKPolyData file (.vtp)')
    parser.add_argument('isovalue', type=float, help='Isovalue for contour extraction')
    
    args = parser.parse_args()
    extract_isocontour(args.input, args.output, args.isovalue)