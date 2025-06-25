import vtk

# Create a single point
points = vtk.vtkPoints()
points.InsertNextPoint(0, 0, 0)

polyData = vtk.vtkPolyData()
polyData.SetPoints(points)

glyphFilter = vtk.vtkVertexGlyphFilter()
glyphFilter.SetInputData(polyData)
glyphFilter.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(glyphFilter.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

window.Render()
interactor.Start()
