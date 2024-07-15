import vtk
from vtk.util import numpy_support
import cv2
import numpy as np

def create_image_actor(image_data, position, rotation_axis, angle):
    # Convert BGR to RGB if necessary
    if image_data.ndim == 3 and image_data.shape[2] == 3:
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

    height, width, _ = image_data.shape
    vtk_image_data = numpy_support.numpy_to_vtk(num_array=image_data.reshape((width * height, 3)), deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(width, height, 1)
    vtk_image.SetSpacing([1, 1, 1])
    vtk_image.SetOrigin([0, 0, 0])
    vtk_image.GetPointData().SetScalars(vtk_image_data)

    texture = vtk.vtkTexture()
    texture.SetInputData(vtk_image)
    texture.InterpolateOn()

    plane = vtk.vtkPlaneSource()
    plane.SetOrigin(0, 0, 0)
    plane.SetPoint1(width, 0, 0)
    plane.SetPoint2(0, height, 0)
    plane.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
    actor.SetPosition(position)
    actor.RotateWXYZ(angle, *rotation_axis)

    return actor

def display_cube(images):
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # Center cube at origin, dimensions 500x500x500
    half_dim = 250
    planes_config = [
        (images[0], [0, 0, half_dim], (1, 0, 0), 0),     # Front
        (images[1], [0, 0, -half_dim], (1, 0, 0), 90),  # Back
        (images[2], [0, 500, -250], (1, 0, 0), 90),    # Top
        (images[3], [0, 0, -250], (0, 1, 0), -90),  # Bottom
        (images[4], [500, 0, -250], (0, 1, 0), -90),  # Left
        (images[5], [0, 0, -250], (0, 1, 0), 0)     # Right
    ]

    for img, pos, axis, ang in planes_config:
        actor = create_image_actor(img, pos, axis, ang)
        renderer.AddActor(actor)

    renderer.SetBackground(0.1, 0.1, 0.1)
    camera = renderer.GetActiveCamera()
    camera.SetPosition(0, 0, 1500)  # Adjust camera position for better viewing
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 1, 0)

    renderer.ResetCamera()
    renderWindow.Render()
    interactor.Start()

# Assuming you have six images, all same size 500x500, and loaded correctly
images = [final_image, expanded_top, expanded_bottom, expanded_left, expanded_right, final_image]  # Replace with correct images
display_cube(images)
