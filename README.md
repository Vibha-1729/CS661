# CS661(Big Data Visual Analytics)
Question 1 \\
This script extracts a 2D isocontour from a 3D .vti (VTK ImageData) volume file and saves the contour as a .vtp (VTK PolyData) file.
The isocontour represents locations in a 2D slice where the scalar field equals a specified isovalue, which can be between [(-1438, 630)].
Command for running the script:
<pre>  python extract_isocontour.py Isabel_2D.vti output.vtp ISOVALUE </pre>
for eg:
python extract_isocontour.py Isabel_2D.vti output.vtp 100

Question 2 \\
The given code renders a 3D scalar field volume data of a Hurricane with optional Phong Shading feature.
In order to run the script, write the line specifying --phong in the command to enable phong shading with the mentioned ambient, diffuse and specular values
<pre> ```bash python task2_Volume_rendering.py Isabel_3D.vti --phong``` </pre>

Don't mention --phong in the command to disable phong shading
<pre> ```bash python task2_Volume_rendering.py Isabel_3D.vti``` </pre>
