import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import os

# 딥러닝 모델 불러오기
model = tf.keras.models.load_model("pet_ex.keras")

# 사진을 저장할 폴더 생성
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# 과거에 테스트한 사진과 결과 저장
if 'past_results' not in st.session_state:
    st.session_state['past_results'] = []

# 사용자 선택 결과 저장
if 'user_selections' not in st.session_state:
    st.session_state['user_selections'] = []

# 이미지 전처리 함수 (224x224로 리사이즈 및 RGBA -> RGB 변환)
def preprocess_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')  # RGBA 등 다른 모드를 RGB로 변환
    image = image.resize((224, 224))  # 모델 입력 크기에 맞게 조정
    image = np.array(image) / 255.0  # 정규화
    image = np.expand_dims(image, axis=0)  # 배치 차원 추가
    return image

# 예측 함수 (모든 클래스 비율 반환)
def predict_emotion(image):
    predictions = model.predict(image)[0]  # 모델의 예측 결과
    emotions = ['Angry', 'Happy', 'Sad', 'Other']  # 클래스 이름
    emotion_confidences = {emotions[i]: predictions[i] * 100 for i in range(len(emotions))}  # 각 감정의 예측 확률 계산
    predicted_emotion = max(emotion_confidences, key=emotion_confidences.get)  # 확률이 가장 높은 감정
    return emotion_confidences, predicted_emotion

# HTML을 이용해 배경색 설정
page_bg = """
<style>
    body {
        background-color: #f9c3ac;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 웹 페이지 제목
st.title("Pet Emotion Classifier")

# 파일 업로드 인터페이스
uploaded_file = st.file_uploader("애완동물 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 사진을 저장하고 화면에 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # 이미지 전처리 및 예측 (224x224로 리사이즈된 이미지 사용)
    preprocessed_image = preprocess_image(image)
    emotion_confidences, predicted_emotion = predict_emotion(preprocessed_image)
    
    # 예측 결과 출력 (모든 감정의 비율 표시)
    st.write("예측 결과:")
    for emotion, confidence in emotion_confidences.items():
        st.write(f"**{emotion}**: {confidence:.2f}%")
    
    st.write(f"가장 확률이 높은 감정: **{predicted_emotion}**")
    
    # 사용자가 직접 감정을 선택할 수 있는 버튼 추가
    st.write("이 사진의 실제 감정을 선택하세요:")
    user_emotion = st.radio("실제 감정 선택:", ('Happy', 'Sad', 'Angry', 'Other'))

    if st.button("선택 완료"):
        st.session_state['user_selections'].append((uploaded_file.name, user_emotion))
        st.write(f"선택하신 감정: {user_emotion}")

    # 결과 저장
    image_path = os.path.join("uploads", uploaded_file.name)
    image.save(image_path)
    st.session_state['past_results'].append((image_path, predicted_emotion, emotion_confidences[predicted_emotion]))

# 오른쪽에 과거 테스트 결과 보여주기
st.sidebar.title("테스트한 이미지들")
st.sidebar.write("여태까지 테스트한 사진들입니다.")
for img_path, emotion, confidence in st.session_state['past_results']:
    st.sidebar.image(img_path, caption=f"{confidence:.2f}%로 {emotion}", use_column_width=True)

# 사용자 선택 결과 보여주기
st.sidebar.write("사용자가 선택한 감정:")
for img_name, user_emotion in st.session_state['user_selections']:
    st.sidebar.write(f"{img_name}: {user_emotion}")
