
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
![Main Gui](https://doc-0o-8c-docs.googleusercontent.com/docs/securesc/o094primfto4ekrfpjtcco78sr956qra/3pnuglo6qtbakb4oovqk81hq6uphh41e/1650688275000/17315809721918653584/17315809721918653584/1wYbsJmzfV7Kj7mLvsSIE2ANUoPp_TIcH?e=view&ax=ACxEAsZBnFXcbK1xx_rXxxISyRDGyIam1wzSjIr6RuWgHhXLkF8uc9M0yJ6lYs7Zzx8_Rr16Yz938p25VywM7djbluaxF5L6tyirEmPa_k5DqMMRhOGXR0e0T2R5msr75jL5k-9SMhu_CQ2D5vCqqXtz9Y20tw3LAfNj7SQaXuEHJZHauQKXafVMLQ_f6P4I34yLJS97GjSjqOZEkcV_ip_tIbELzuxCKW__HyZVxyu4eebHla1mXtJ3_KSOdC9qPrd9w9qKSA2kkcJVxwzXcSBzPoi9ZBfVicaGIKkXQ-o61NDs_CYzIT9g5YvO1iHo2B9k2tei7OKONVuLiciuVrNcE1juJluqsrmCxyXXkhqMgYelXZNJTSF6jEPQzYjpeYqhdST-sPyyqXgWEKk1WHijih4nErjLd41FM7uVzBu6H_s5KCdefiw6rsCA9IpPJxN_6YH7i0TzPoNfqJGjVSYoUTJ9636flWZ8tRVNzqsK2DYa-hg7fVpHJsITj1GzxnccXvzOi4nuSNXxXPPFGgeGRcAjmYigjOPvN8f7tQk1hzLJfKmkqv7dvIL4ckimqhLBX4F1b714nG0VmljBT5_xWDaULR5EpTEsPvYOFwKQYcxagu7mZSI00P3Ukj6_FiQO9NnZ55f-SVM2G8xtvcdnGuQobsHo0PBQC5k-oJJD5W5cIu-Vc8ugAsT2YTlVw5c5hly-jRtdP4y3srBu8BLUvSvBH9zEz1GnpJd75KNxPVLMPen7ekK2DKqe6wcUlWmzl-VFMLXwxAy8K-5v6m5WOR-YXbwptdTwh46I7SL0rY8l5TJ70rNVVcUvZHcv6DWBStlZrD26wb_NDSXVnUa5BOaGPRw&authuser=0&nonce=rd5tifuq764ss&user=17315809721918653584&hash=ips682rkp7mrjvvtufa97vi3dlji5qta)
[![Test][Squat Example]](https://drive.google.com/uc?export=view&id=1JokEDiSxRQDm_ZfrLQwFEWN2J_e_Hmbv)

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

