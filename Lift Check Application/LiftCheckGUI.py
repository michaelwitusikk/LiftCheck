import PySimpleGUI as sg # GUI library
from FormScripts import bicepCurlForm as bf
from FormScripts import overallPoseRendering as pr

bicep_curl_image = 'Lift Check Application/GUIphotos/bicepCurl.png'
squat_image = 'Lift Check Application/GUIphotos/squatForm.png'


def main():
    
    layout = [[sg.Titlebar('Lift Check', key='-text-')], 
              [sg.Button("Pose Renderings"), sg.Button("Squat Form", image_filename=squat_image, image_subsample=3), 
               sg.Button("Bicep Curl Form", image_filename=bicep_curl_image, image_subsample=3), 
               sg.Button("Push up Form")]]

    # Create the window
    window = sg.Window("Lift Check v1.0", layout, size=(800,600))

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Pose Renderings":
            pr.poseRendering()
        if event == "Bicep Curl Form":
            bf.bicepRendering()
            
    window.close()

if __name__ == "__main__":
    main()