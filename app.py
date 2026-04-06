from flask import Flask, request, jsonify, render_template
import threading
import os

from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
print("DEBUG MONGO URL:", os.getenv("MONGODB_URL"))

training_status = {
    "status": "idle",   # idle | running | completed | cancelled
    "progress": 0
}

MODEL_PATH = "artifacts/model.pkl"


@app.route('/')
def home():
    model_exists = os.path.exists(MODEL_PATH)
    return render_template('index.html', model_exists=model_exists)


# 🔴 START TRAINING (REAL PROGRESS)
@app.route('/start_training')
def start_training():

    def run_training():
        global training_status

        try:
            training_status["status"] = "running"
            training_status["progress"] = 0

            pipeline = TrainingPipeline()

            # STEP 1
            if training_status["status"] == "cancelled":
                return
            training_status["progress"] = 10
            raw_data = pipeline.start_data_ingestion()

            # STEP 2
            if training_status["status"] == "cancelled":
                return
            training_status["progress"] = 30
            valid_data = pipeline.start_data_validation(raw_data)

            # STEP 3
            if training_status["status"] == "cancelled":
                return
            training_status["progress"] = 60
            train_arr, test_arr, preprocessor = pipeline.start_data_transformation(valid_data)

            # STEP 4
            if training_status["status"] == "cancelled":
                return
            training_status["progress"] = 90
            pipeline.start_model_trainer(train_arr, test_arr, preprocessor)

            # DONE
            training_status["progress"] = 100
            training_status["status"] = "completed"

        except Exception as e:
            training_status["status"] = "idle"
            print("❌ ERROR:", e)

    threading.Thread(target=run_training).start()
    return jsonify({"message": "Training started"})


# 🔴 GET STATUS
@app.route('/training_status')
def get_status():
    return jsonify(training_status)


# 🔴 CANCEL
@app.route('/cancel_training')
def cancel_training():
    training_status["status"] = "cancelled"
    return jsonify({"message": "Training cancelled"})


# 🔴 PREDICT
@app.route('/predict', methods=['POST'])
def predict():

    if not os.path.exists(MODEL_PATH):
        return "❌ Model not found. Please train first."

    data = request.form
    prediction_pipeline = PredictionPipeline(data)
    prediction = prediction_pipeline.run_pipeline()

    return render_template('result.html', prediction=f"{prediction[0]:.3f}")


if __name__ == "__main__":
    print("👉 Open: http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)