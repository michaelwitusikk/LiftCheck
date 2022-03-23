import PySimpleGUI as sg # GUI library
from FormScripts import bicepCurlForm as bf
from FormScripts import overallPoseRendering as pr
from FormScripts import squatForm as sf

bicep_curl_image = 'Lift Check Application/GUIphotos/bicepCurl.png'
squat_image = 'Lift Check Application/GUIphotos/squatForm2.png'


def main():
    
    layout = [[sg.Titlebar('Lift Check', key='-text-')], 
              [sg.Button(" ", image_filename=squat_image, image_subsample=2),
               sg.Button("  ", image_filename=bicep_curl_image, image_subsample=2)]
               ,[sg.Text('Number of Reps:',font=('Helvetica', 20))],[[sg.Slider(range=(3,12),default_value=6,size=(20,15),orientation='horizontal',font=('Helvetica', 20))],],
               [sg.Checkbox("Draw Pose?", font=('Helvetica', 20),pad=15, default=True)]]

    # Create the window
    window = sg.Window("Lift Check v1.0", layout, size=(800,600))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or presses q

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
         # This is squat event
        if event == " ":
            sf.squat_render(values[0],values[1])
        # This is curl event
        if event == "  ":
            bf.bicepRendering(values[0],values[1])
            
    window.close()

if __name__ == "__main__":
    main()