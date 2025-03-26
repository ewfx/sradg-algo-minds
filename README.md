
# 🚀 Smarter Reconciliation and Anomaly Detection using Gen AI

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)


---

## 🎯 Introduction
## Smarter Reconciliation and Anomaly Detection using Gen AI
Financial reconciliation involves processing large transaction volumes, requiring manual effort to detect and resolve anomalies, making the process time-consuming and error-prone. To address this, we leverage Machine Learning and Generative AI to automate anomaly detection, analyze historical patterns, and provide intelligent insights for faster and more accurate reconciliation.

### Problem Statement
Existing reconciliation tools process vast amounts of transactions but require significant manual effort to identify and resolve anomalies. The goal is to implement an AI-driven anomaly detection system that automates this process using historical data, reducing manual work and improving accuracy.

### Proposed Approach
•	Interactive Feedback: Develop an application for reconcilers to check for anomalies, understand its root cause, give feedback, and take actions on the anomaly.

•	Clustering & Analysis: Implemented clustering algorithms like Isolation Tree and Autoencoders to detect anomalies.

•	Leverage AI Models: Used the Hugging Face LLM model to detect anomaly categories and find the root cause.



## 🎥 Demo
📹 [Video Demo](#) (if applicable)  



🖼️ Screenshots:

### Step 1: Add Reconciliation data 
After processing the data, Match staus and Anomaly category is populated
![image](https://github.com/user-attachments/assets/74c14392-37fe-4c41-a598-dd2a1690bc25)

### Step 2: Allows Edit 
Options to mark data as False positive, also can update anomaly category and comments
![image](https://github.com/user-attachments/assets/2301617c-395b-4da0-955b-f876c7bb4fdd)

### Step 3: Add new anomaly category 
User can even add anomaly category by there own
![image](https://github.com/user-attachments/assets/235bd536-b59e-4bf2-87f3-44f6b93aaa79)

### Step 3: Get updated excel output 
After all the processing, user can get updated data as excel
![image](https://github.com/user-attachments/assets/3087925f-faf5-4487-b3c8-aa5184510e53)



## ⚙️ What It Does


✅ **Detects anomalies** using Isolation Forest and other Autoencodes on historical and real-time reconciliation data.  
✅ **Classifies anomalies** into predefined categories based on business rules and historical trends.  
✅ **Generates AI-driven insights** using LLM to assist in anomaly Type.  
✅ **Supports file uploads and downloads** via interactive UI 
✅ **Provides rule-based recommendations** for reconcilers to address mismatches efficiently.  
✅ **Enables real-time updates**, allowing row-level modifications and dynamic data refresh.  
✅ **Automates email notifications** to alert users on anomaly detection, updates, and resolutions.  



## 🛠️ How We Built It

🖼️ Application Flow:
![Application Flow](https://github.com/user-attachments/assets/cc70e232-8e2a-4b75-a14f-a1bad5f61f9e)

- **ML & GenAI** – Leverages Machine Learning and Generative AI to detect anomalies and provide insights into potential root causes.  
- **Programming Language** – Developed in **Python** for model training, inference, and API deployment.  
- **Frameworks & Libraries** –  
  - **Flask** – Deploys APIs for real-time anomaly detection and reconciliation processing.  
  - **Pandas** – Handles data processing, cleaning, and transformation for reconciliation.  
  - **Scikit-learn** – Implements anomaly detection models such as Isolation Forest.  
  - **Hugging Face** – Utilized for AI-driven insights and text-based anomaly explanations.  
- **Frontend (React UI)** –  
  - **React.js** – Builds an interactive and responsive UI for visualizing anomalies and reconciliation insights.  
- **Dataset** – Uses a combination of generated historical and real-time reconciliation data for model training, evaluation, and validation.

## 🚧 Challenges We Faced
- **Data Quality Issues** – Unavailability of quality financial data for training the model.
- **Flexible File Handling** – Supports dynamic file paths and ensures seamless management of user-uploaded datasets.  
- **Reliable AI Responses** – Ensures OpenAI-generated prompts return valid and structured JSON consistently.  
- **Consistent Data Mapping** – Maintains uniformity in `MatchStatus` classifications and anomaly bucket mappings.  
- **Robust Data Handling** – Manages missing values, mixed data types, and multiple date formats in reconciliation files.  
- **Scalable Real-Time Updates** – Enables dynamic row-level modifications and ensures proper deletion upon resolution.  
- **Domain-Specific Rule Engine** – Implements meaningful, rule-based logic that aligns with business reconciliation processes.  
- **Optimized Performance** – Enhances processing efficiency to handle large-scale reconciliation data with minimal latency.  
- **Seamless Integration** – Designed to work with existing reconciliation tools while maintaining high flexibility and adaptability

## 🏃 How to Run

1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/sradg-algo-minds.git
   ```
2. Run the Python backend 
   ```sh
   cd code/src/backend
   ```
3. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
4. Run the backend server  
   ```sh
   python app.py
   ```
5. Run the React frontend 
   ```sh
   cd code/src/frontend
   ```
6. Install dependencies  
   ```sh
   npm install
   ```
7. Run the project  
   ```sh
   npm start
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React
- 🔹 Backend: Flask
- 🔹 Machine Learning: Isolation Forest, Autoencoder
- 🔹 Gen AI: Hugging Face API


## 👥 Team

- 👨‍💻 **Palash Bajpai** – [GitHub](https://github.com/PALASH-BAJPAI)
- 👨‍💻 **Krishna Sahani** – [GitHub](https://github.com/krishna0303)
- 👨‍💻 **Prasad Chadaram**
- 👨‍💻 **Nitesh Jha**
