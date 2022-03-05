import csv
import os
import cv2
import numpy as np
from tqdm import tqdm

def read_video(video_filename, width=112, height=112,):
  """Read video from file."""
  cap = cv2.VideoCapture(video_filename)
  fps = cap.get(cv2.CAP_PROP_FPS)
  #width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  frames = []
  if cap.isOpened():
    while True:
      success, frame_bgr = cap.read()
      if not success:
        break
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      frame_rgb = cv2.resize(frame_rgb, (width, height))
      frames.append(frame_rgb)
  frames = np.asarray(frames)
  return frames, fps, width, height

splits = ["train", "test", "val"]
for split in splits:
    with open("CountixAV_"+split + ".csv") as origin_csv:
        with open("CountixAV_"+split+"_processed.csv", "w+") as write_csv:
            save_dir = '/Storage/yhx/Datasets/countix_AV/countixAV_'+split+"_segments/"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            s_csv = csv.writer(write_csv)
            f_csv = csv.reader(origin_csv)
            f_csv.__next__()
            for i, row in enumerate(f_csv):
                video_mp4 = '/Storage/yhx/Datasets/countix_AV/countixAV_'+split+"/"+row[0]+".mp4"
                video_mkv = '/Storage/yhx/Datasets/countix_AV/countixAV_'+split+"/"+row[0]+".mkv"
                if os.path.exists(video_mp4) or os.path.exists(video_mkv) :
                    video,fps, width, height = read_video(video_mp4 if os.path.exists(video_mp4) else video_mkv)
                    """ for index in range(2, 6):
                        row[index] *= fps"""
                    print(row[2], row[3])
                    row[0] = "_".join([row[0], str(row[2]), str(row[3])])
                    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                    out = cv2.VideoWriter(os.path.join(save_dir, row[0] + '.mp4'), fourcc, fps, (width, height))
                    for frame in video[int(int(row[2])*fps): int(int(row[3])*fps+1)]:
                        out.write(frame)
                    row.append(row[1])
                    row.append(row[1])
                    row.pop(1)
                    s_csv.writerow(row)
                    out.release()
