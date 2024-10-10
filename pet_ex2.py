import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np

# 딥러닝 모델 불러오기
model = tf.keras.models.load_model("pet_ex.keras")

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

# 웹 페이지 제목
st.title("Pet Emotion Classifier")

# 파일 업로드 인터페이스
uploaded_file = st.file_uploader("애완동물 사진을 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지를 메모리에서 바로 처리
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # 이미지 전처리 및 예측
    preprocessed_image = preprocess_image(image)
    emotion_confidences, predicted_emotion = predict_emotion(preprocessed_image)

    # 예측 결과 출력
    st.write("예측 결과:")
    for emotion, confidence in emotion_confidences.items():
        st.write(f"**{emotion}**: {confidence:.2f}%")
    
    st.write(f"가장 확률이 높은 감정: **{predicted_emotion}**")
