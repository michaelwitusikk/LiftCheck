
# About Lift Check

Lift Check is a form tracking application built to detect improper movement
across a variety of exercises. The project is built in python utilizing PySimpleGUI, OpenCV, and MediaPipe.
Users can get live, real-time feedback as they work out or input previously recorded
video to be analyzed.


## Usage/Examples
Dependencies
- [OpenCV](https://github.com/opencv/opencv)
- [MediaPipe](https://github.com/google/mediapipe)
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
- [gTTS](https://github.com/pndurette/gTTS)
- [Numpy](https://github.com/numpy/numpy)

Clone Repo. Install dependencies to python enviroment. For live video, webcam permissions
must be granted. (MacOS -> Visual Studio "Add code to path", run "code" in terminal)

To run the project: 
```shell
python3 LiftCheckGUI.py
```
Set number of repititions, draw pose skeleton on video option, and browse for video input.
![Main Gui](https://drive.google.com/uc?export=view&id=1wYbsJmzfV7Kj7mLvsSIE2ANUoPp_TIcH)
![Squat Example](https://drive.google.com/uc?export=view&id=1JokEDiSxRQDm_ZfrLQwFEWN2J_e_Hmbv)

```shell
Reps:
Rep #1: Perfect! Depth Angle: 57.0
Rep #2: Not to depth (90 degrees or below),  Depth Angle: 162.0
Rep #3: Perfect! Depth Angle: 54.0
Rep #4: Not to depth (90 degrees or below),  Depth Angle: 162.0
Rep #5: Perfect! Depth Angle: 46.0
Rep #6: Perfect! Depth Angle: 50.0
```
For best results, use high contrast backgroud, with only one person visible. Entire body must be in frame.
Videos of squat, bicep curl must be front facing, squat can be from left side portrait.

## Authors

- [@ManuelPerez](https://github.com/pm9013163)
- [@MichaelWitusik](https://github.com/michaelwitusikk)


## License

[GNU General Public License v3.0](https://github.com/michaelwitusikk/LiftCheck/blob/main/LICENSE)

