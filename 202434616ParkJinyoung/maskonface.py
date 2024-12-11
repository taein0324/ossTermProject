import cv2
import mediapipe as mp

# 얼굴 검출을 위한 객체
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    static_image_mode=True,
    max_num_faces=1,
)

mp_drawing = mp.solutions.drawing_utils

# 이미지 읽기
image = cv2.imread("image2.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = face_mesh.process(image_rgb)

mask_image = cv2.imread('mask.png', cv2.IMREAD_UNCHANGED)

# 랜드마크만 그린 이미지 저장
image_landmarks_only = image.copy() 
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image_landmarks_only,
            landmark_list=face_landmarks,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),

        )

cv2.imwrite("image2_with_landmark.jpg", image_landmarks_only)

def apply_mask_to_face(image, landmarks, mask_image):
    height, width, _ = image.shape
    mask_height, mask_width, _ = mask_image.shape

    # 코끝과 입술의 위치를 기준으로 마스크를 위치시킴
    nose_tip = landmarks[1]  # 코끝 랜드마크
    upper_lip = landmarks[0]  # 윗입술
    bottom_lip = landmarks[17]  # 아랫입술

    # 코와 입술의 중심점 계산
    center_x = int((upper_lip[0] + bottom_lip[0]) * width / 2)
    center_y = int((upper_lip[1] + bottom_lip[1]) * height / 2)

    # 코끝에서 입술까지의 거리와 얼굴 비율을 고려해 크기 결정
    nose_to_lip_distance = abs(int(nose_tip[1] * height) - int(upper_lip[1] * height))
    scale_factor = nose_to_lip_distance * 10 

    # 마스크 크기 조정
    mask_resized = cv2.resize(mask_image, None, fx=scale_factor / mask_width, fy=scale_factor / mask_height)

    mask_height, mask_width, _ = mask_resized.shape

    top_left_x = center_x - mask_width // 2
    top_left_y = int(nose_tip[1] * height) - mask_height // 2 
    if top_left_x < 0:
        top_left_x = 0
    if top_left_y < 0:
        top_left_y = 0
    if top_left_x + mask_width > width:
        top_left_x = width - mask_width
    if top_left_y + mask_height > height:
        top_left_y = height - mask_height

    for c in range(0, 3):
        alpha = mask_resized[:, :, 3] / 255.0  
        image[top_left_y:top_left_y + mask_height, top_left_x:top_left_x + mask_width, c] = (
            alpha * mask_resized[:, :, c] + (1 - alpha) * image[top_left_y:top_left_y + mask_height, top_left_x:top_left_x + mask_width, c]
        )

    return image


if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        landmarks = [(lm.x, lm.y) for lm in face_landmarks.landmark]

        image_with_mask = apply_mask_to_face(image, landmarks, mask_image)


cv2.imwrite("image2_with_mask.jpg", image_with_mask)
