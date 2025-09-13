# Next-Gen Health Surveillance

**Augmented Reality Meets AI for Predictive Heart Attack Analytics**

## 📌 Overview

This project introduces an advanced **IoT–AI–AR based health monitoring system** designed for real-time **heart attack prediction and visualization**. By integrating **ECG and temperature sensors**, **AI-driven predictive models**, and **Augmented Reality (AR)** visualization, the system helps healthcare providers monitor patients (especially bedridden or critical ones) with **minimal delay in emergencies**.

## ✨ Features

* 📊 **Real-time Health Monitoring** using ECG (AD8232) & Temperature (DHT11) sensors.
* 🤖 **AI-powered prediction model** (Bagging Classifier) trained on Kaggle heart disease dataset with **98.58% accuracy**.
* ☁️ **Cloud integration** using **Firebase Realtime Database** for live data updates.
* 📱 **Augmented Reality App** (Unity + Vuforia) that visualizes patient vitals in 3D after scanning a QR/image target.
* 🌐 **Web Application** (HTML, CSS, JS, Django backend) for interactive patient risk assessment.
* ⚡ **Low-cost and scalable solution** for healthcare monitoring in critical care settings.

## 🛠️ Tech Stack

* **Hardware:** Arduino UNO, ECG Sensor (AD8232), DHT11 Sensor, LCD Display, ESP-12E NodeMCU (ESP8266).
* **Software & Tools:** Arduino IDE, Firebase, Unity 3D, Vuforia SDK, Python (Django), HTML, CSS, JavaScript.
* **AI/ML Model:** Bagging Classifier trained on **1025 patient records with 14 attributes**.

## 📐 System Architecture

1. **Sensors (ECG + DHT11)** → Arduino UNO → NodeMCU (ESP8266).
2. **Data Transmission** → Firebase Realtime Database.
3. **AI Model (Bagging Classifier)** → Predicts heart attack risk.
4. **AR Mobile App (Unity + Vuforia)** → Visualizes vitals in real-time.
5. **Web App (Django + Frontend)** → Displays prediction results and patient status.

## 📊 Results

* Achieved **98.58% accuracy** with Bagging Classifier for heart attack prediction.
* Successful **real-time AR visualization** of heart rate, temperature, and abnormalities.
* Enabled **seamless integration** of IoT, AI, AR, and cloud storage for healthcare monitoring.

## 🚀 Future Enhancements

* Integration of additional biosensors (Cholesterol, Blood Pressure, Blood Sugar).
* Development of **wearable devices** for continuous health monitoring.
* Incorporation of **Troponin biosensors** for more precise heart attack detection.
* Enhanced **telemedicine integration** with AR-based remote consultations.
* Blockchain-based **secure health data management**.

## 👨‍💻 Team Members

* **Vinusa S**
* **Kamalesh A**
* **Tamil Vani I**
* **Goutham G S**

## 📜 License

This project is created as part of **Bachelor of Engineering in Biomedical Engineering** (Anna University, Chennai – 2025). Free to use for academic and research purposes with proper citation.
