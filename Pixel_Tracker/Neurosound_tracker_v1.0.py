import os
import sys
import subprocess

try:
    # 없는 모듈 import시 에러 발생
    import cv2
except:
    # pip 모듈 업그레이드
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', 'pip'])
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', 'opencv-contrib-python'])

try:
    # 없는 모듈 import시 에러 발생
    import tkinter
except:
    # 에러 발생한 모듈 설치
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', 'tkinter'])


from tkinter import filedialog
import tkinter as tk

import warnings
warnings.filterwarnings('ignore')

root = tk.Tk()
root.withdraw()

root.file = filedialog.askopenfile(
    initialdir=f'{os.getcwd()}',  # 현재창
    title="파일 선택창",
    filetypes=(("data files", "*.mp4"), ("all files", "*.*")))

print(root.file.name)

# 트랙커 객체 생성자 함수 리스트 ---①
trackers = [cv2.legacy.TrackerBoosting_create,
            cv2.legacy.TrackerMIL_create,
            cv2.legacy.TrackerKCF_create,
            cv2.legacy.TrackerTLD_create,
            cv2.legacy.TrackerMedianFlow_create,
            cv2.legacy.TrackerCSRT_create,
            cv2.legacy.TrackerMOSSE_create]
trackerIdx = 0  # 트랙커 생성자 함수 선택 인덱스
tracker = None
isFirst = True

video_src = 0  # 비디오 파일과 카메라 선택
video_src = root.file.name
cap = cv2.VideoCapture(video_src)
fps = cap.get(cv2.CAP_PROP_FPS)  # 프레임 수 구하기
delay = int(1000 / fps)
win_name = 'tracker no.1'

while cap.isOpened():
    # 비디오실행
    ret, frame = cap.read()
    if not ret:
        print('Cannot read video file')
        break

    img_draw = frame.copy()

    if tracker is None:  # 트랙커 생성 안된 경우
        cv2.putText(img_draw, "Press the Space to set ROI!!",
                    (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

    else:
        ok, bbox = tracker.update(frame)   # 새로운 프레임에서 추적 위치 찾기 ---③
        (x, y, w, h) = bbox

        if ok:  # 추적 성공
            cv2.rectangle(img_draw, (int(x), int(y)), (int(x + w), int(y + h)),
                          (0, 255, 0), 2, 1)
            cv2.putText(img_draw, str(int(roi[0])-int(x)) + " pixels", (350, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0), 2, cv2.LINE_AA)

        else:  # 추적 실패
            cv2.putText(img_draw, "Tracking fail.", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

    trackerName = tracker.__class__.__name__
    cv2.putText(img_draw, str(trackerIdx) + ":"+trackerName, (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow(win_name, img_draw)
    key = cv2.waitKey(delay) & 0xff

    # 스페이스 바 또는 비디오 파일 최초 실행 ---④
    if key == ord(' ') or (video_src != 0 and isFirst):
        isFirst = False
        roi = cv2.selectROI(win_name, frame, False)  # 초기 객체 위치 설정
        if roi[2] and roi[3]:         # 위치 설정 값 있는 경우
            tracker = trackers[trackerIdx]()  # 트랙커 객체 생성 ---⑤
            isInit = tracker.init(frame, roi)

    elif key in range(48, 56):  # 0~6까지
        trackerIdx = key-48     # 선택한 숫자로 트랙커 인덱스 수정

        if bbox is not None:
            tracker = trackers[trackerIdx]()  # 선택한 숫자의 트랙커 객체 생성 ---⑦
            isInit = tracker.init(frame, bbox)  # 이전 추적 위치로 추적 위치 초기화

    elif key == 27:  # esc로 종료
        break

else:
    print("Could not open video")

f = open('output.txt', 'w')
print(f'move {int(roi[0])-int(x)} pixels', file=f)
f.close()

cap.release()
cv2.destroyAllWindows()

root.mainloop()
os.system('taskkill /f /im tracker_v1.0.exe')
