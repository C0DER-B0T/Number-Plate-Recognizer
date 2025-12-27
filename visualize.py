import ast
import cv2
import numpy as np
import pandas as pd
import os

# --- 1. SETTINGS ---
VIDEO_PATH = 'sample03.mp4'      # Make sure this matches your video file name exactly!
CSV_PATH = './test.csv'        # We use test.csv since main.py usually outputs this
OUTPUT_PATH = './out.mp4'

def draw_border(img, top_left, bottom_right, color=(0, 255, 0), thickness=10, line_length_x=200, line_length_y=200):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)
    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)
    return img

# --- 2. VERIFY FILES EXIST ---
if not os.path.exists(CSV_PATH):
    print(f"❌ ERROR: Could not find {CSV_PATH}. Did you run main.py successfully?")
    exit()

if not os.path.exists(VIDEO_PATH):
    print(f"❌ ERROR: Could not find {VIDEO_PATH}. Check your file name!")
    exit()

try:
    results = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded {len(results)} rows from {CSV_PATH}")
except Exception as e:
    print(f"❌ ERROR reading CSV: {e}")
    exit()

# --- 3. SETUP VIDEO ---
cap = cv2.VideoCapture(VIDEO_PATH)
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 'mp4v' is safest for Linux/Codespaces
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# --- 4. PRELOAD LICENSES ---
license_plate = {}
for car_id in np.unique(results['car_id']):
    max_ = np.amax(results[results['car_id'] == car_id]['license_number_score'])
    
    # Get the row with the best score
    best_row = results[(results['car_id'] == car_id) & (results['license_number_score'] == max_)].iloc[0]
    
    license_plate[car_id] = {
        'license_crop': None,
        'license_plate_number': best_row['license_number']
    }
    
    # Go to the frame where this best license plate was seen
    cap.set(cv2.CAP_PROP_POS_FRAMES, best_row['frame_nmr'])
    ret, frame = cap.read()
    
    if ret:
        x1, y1, x2, y2 = ast.literal_eval(best_row['license_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
        
        # Crop and resize
        crop = frame[int(y1):int(y2), int(x1):int(x2), :]
        crop = cv2.resize(crop, (int((x2 - x1) * 400 / (y2 - y1)), 400))
        license_plate[car_id]['license_crop'] = crop

# --- 5. PROCESS FRAMES ---
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
frame_nmr = -1
print("Processing video... this might take a minute.")

while True:
    ret, frame = cap.read()
    frame_nmr += 1
    if not ret:
        break
        
    df_ = results[results['frame_nmr'] == frame_nmr]
    
    for row_indx in range(len(df_)):
        try:
            # Draw Car Border
            car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(df_.iloc[row_indx]['car_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), (0, 255, 0), 25, line_length_x=200, line_length_y=200)

            # Draw License Box
            x1, y1, x2, y2 = ast.literal_eval(df_.iloc[row_indx]['license_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 12)

            # Draw Crop & Text
            car_id = df_.iloc[row_indx]['car_id']
            if car_id in license_plate and license_plate[car_id]['license_crop'] is not None:
                license_crop = license_plate[car_id]['license_crop']
                H, W, _ = license_crop.shape

                # Paste the license plate crop on screen
                frame[int(car_y1) - H - 100:int(car_y1) - 100,
                      int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2), :] = license_crop
                
                # White background for text
                frame[int(car_y1) - H - 400:int(car_y1) - H - 100,
                      int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2), :] = (255, 255, 255)

                # Text (Small Font for Indian Plates)
                text = license_plate[car_id]['license_plate_number']
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2.0, 6)
                
                cv2.putText(frame, text,
                            (int((car_x2 + car_x1 - text_width) / 2), int(car_y1 - H - 250 + (text_height / 2))),
                            cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 6)
        except Exception as e:
            pass # Skip errors on single frames

    out.write(frame)
    if frame_nmr % 100 == 0:
        print(f"Processed {frame_nmr} frames...")

out.release()
cap.release()
print(f"✅ Success! Download {OUTPUT_PATH} to watch your video.")