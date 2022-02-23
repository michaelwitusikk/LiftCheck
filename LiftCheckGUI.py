import PySimpleGUI as sg # GUI library
import overallPoseRendering as pr
import bicepCurlForm as bf

def main():
    
    layout = [[sg.Titlebar('Lift Check', key='-text-')], [sg.Button("Pose Renderings"), sg.Button("Squat Form"), sg.Button("Bicep Curl Form"), sg.Button("Push up Form")]]

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