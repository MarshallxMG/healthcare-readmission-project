# Healthcare Readmission Project

This project is a machine learning-powered application designed to predict the likelihood of patient readmission. It features a React frontend for user interaction and a FastAPI backend for serving predictions.

## Features

-   **Readmission Prediction:** Uses a trained machine learning model to estimate readmission probability.
-   **Interactive UI:** User-friendly interface built with React.
-   **Real-time Analysis:** Fast predictions served via FastAPI.
-   **Data Visualization:** Visual representation of risk factors.

## Tech Stack

### Frontend
-   **React**
-   **Chart.js / Recharts** (for visualizations)
-   **CSS / Tailwind** (for styling)

### Backend
-   **FastAPI**
-   **Python**
-   **Scikit-learn** (Machine Learning)
-   **Pandas / NumPy** (Data Processing)

## Installation & Setup

### Prerequisites
-   Node.js & npm
-   Python 3.8+

### Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MarshallxMG/healthcare-readmission-project.git
    cd healthcare-readmission-project
    ```

2.  **Install Dependencies:**
    ```bash
    npm run install-all
    ```
    *This script installs dependencies for both the frontend and backend.*

3.  **Run the Application:**
    ```bash
    npm start
    ```
    *This will start both the FastAPI backend and the React frontend concurrently.*

## Project Structure

-   `frontend/`: React application source code.
-   `backend/`: FastAPI application and model inference logic.
-   `model/`: Trained machine learning models (`.pkl` files).
-   `data/`: Dataset files (if applicable).

## License

[MIT](LICENSE)
