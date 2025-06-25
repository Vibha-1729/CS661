import vtk

# Define the 4 corner points (Z = 25)
points = vtk.vtkPoints()
points.InsertNextPoint(0.0, 0.0, 25.0)  # bottom-left
points.InsertNextPoint(1.0, 0.0, 25.0)  # top-left
points.InsertNextPoint(0.0, 1.0, 25.0) # bottom-right
points.InsertNextPoint(1.0, 1.0, 25.0) # top-right

# Create color array
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)  # RGB
colors.SetName("Colors")

# Assign distinct colors to each point
colors.InsertNextTuple3(255, 0, 0)   # red
colors.InsertNextTuple3(0, 255, 0)   # green
colors.InsertNextTuple3(0, 0, 255)   # blue
colors.InsertNextTuple3(0, 255, 255) # cyan

# Create a polydata object and add points and colors
polyData = vtk.vtkPolyData()
polyData.SetPoints(points)
polyData.GetPointData().SetScalars(colors)

# Glyph filter to show points
glyphFilter = vtk.vtkVertexGlyphFilter()
glyphFilter.SetInputData(polyData)
glyphFilter.Update()

# Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(glyphFilter.GetOutputPort())

# Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(15)

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)  # white background

# Render window and interactor
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Start rendering
renderWindow.Render()
interactor.Start()
