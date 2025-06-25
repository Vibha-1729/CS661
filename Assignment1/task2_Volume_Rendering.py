import vtk
import argparse

def setup_color_transfer_function():
    ctf = vtk.vtkColorTransferFunction()
    ctf.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    ctf.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    ctf.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
    ctf.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    ctf.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    ctf.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)
    return ctf

def setup_opacity_transfer_function():
    otf = vtk.vtkPiecewiseFunction()
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(101.815, 0.002)
    otf.AddPoint(2594.97, 0.0)
    return otf

def volume_render(input_file, use_phong):
    # Read the input volume data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    # Create volume mapper
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())
    
    # Create volume property
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(setup_color_transfer_function())
    volume_property.SetScalarOpacity(setup_opacity_transfer_function())
    volume_property.ShadeOn()
    
    if use_phong:
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    
    # Create volume
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)
    
    # Create outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    
    # Create renderer
    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.AddActor(outline_actor)
    renderer.SetBackground(0.1, 0.1, 0.1)
    
    # Create render window
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)
    
    # Create interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    
    # Start rendering
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Volume rendering with VTK')
    parser.add_argument('input', help='Input VTKImageData file (.vti)')
    parser.add_argument('--phong', action='store_true', 
                       help='Enable Phong shading (default: False)')
    
    args = parser.parse_args()
    
    volume_render(args.input, args.phong)