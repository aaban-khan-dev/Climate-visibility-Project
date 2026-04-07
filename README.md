# 🌍 Climate Visibility Prediction System

## 📌 Overview
This project focuses on predicting **visibility distance** using climatic and environmental factors such as temperature, humidity, wind speed, and pressure.

The goal is to build an **end-to-end machine learning system** that can assist in real-world applications like:
- Aviation safety  
- Road transportation  
- Maritime navigation  
- Smart city systems  

---

## 🚀 Key Features
- End-to-end ML pipeline (data → training → prediction)  
- Data storage using MongoDB  
- Model and artifacts storage using AWS S3  
- Automated training and prediction pipelines  
- API-based deployment using FastAPI  
- Containerization using Docker  
- CI/CD using GitHub Actions  

---

## 🧠 Problem Statement
Predict **maximum visibility distance** based on:
- Temperature  
- Relative Humidity  
- Wind Speed  
- Atmospheric Pressure  
- Other environmental factors  

This helps improve **decision-making in safety-critical environments**.

---

## 🏗️ Project Architecture
The system follows a modular pipeline:

1. Data Ingestion (MongoDB / external sources)  
2. Data Validation  
3. Data Transformation  
4. Model Training  
5. Model Evaluation  
6. Model Pushing to AWS S3  
7. Prediction Pipeline  
8. API Deployment (FastAPI)  

---

## ⚙️ Tech Stack

### Programming & Frameworks
- Python  
- FastAPI / Flask  

### Machine Learning
- Scikit-learn  
- XGBoost  

### Cloud & Storage
- AWS S3  
- MongoDB  

### DevOps & Tools
- Docker  
- GitHub Actions  
- Terraform (for infrastructure)  

---

## 📊 Workflow

### Training Pipeline
- Fetch data from MongoDB  
- Perform preprocessing & feature engineering  
- Train ML models  
- Evaluate performance  
- Store model and artifacts in S3  

### Prediction Pipeline
- Load model from S3  
- Accept user input via API  
- Return predicted visibility  

---

## 🌐 API Endpoints

### `/train`
- Triggers model training pipeline  

### `/predict`
- Accepts input features and returns predicted visibility  

---

## 🖥️ Demo

The system provides a web interface where users can input:
- Temperature  
- Humidity  
- Wind Speed  
- Pressure  

And get predicted visibility instantly.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/climate-visibility.git
cd climate-visibility
pip install -r requirements.txt

```

📈 Future Scope
Real-time data integration
Advanced deep learning models
Integration with smart city systems
Improved model monitoring and drift detection

---

👨‍💻 Author
Mohammad Aaban
