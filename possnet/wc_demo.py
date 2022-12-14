import sys; sys.path.insert(1, '../')
from helper.crop_utils import crop_square

import time
import cv2
from pose_manager import PoseManager


WEBCAM_HEIGHT = 480
WEBCAM_WIDTH = 640

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FPS, 60)

pose_manager = PoseManager()
    
while True:    
    ret, frame = cap.read()
    
    h, w, _ = frame.shape
    assert h == WEBCAM_HEIGHT
    
    frame = crop_square(frame)    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    t1 = time.time()
    pose_scores, keypoint_scores, keypoint_coords = pose_manager(frame_rgb)
    t2 = time.time() - t1    

    pose_manager.draw_keypoints(frame_rgb, pose_scores, keypoint_scores, keypoint_coords)
    
            
    cv2.putText(frame_rgb,"frame_time: {:.0f} ms".format(t2*1000),(10,50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow("result", cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
    

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):      
        cap.release()
        cv2.destroyAllWindows()
        break
    
