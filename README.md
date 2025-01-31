# 🌐 Language Translation 

This project is a **language translation application** built using **FastAPI** (backend) and **Streamlit** (frontend). It leverages **Facebook's MBART model** for translation and stores results in **MongoDB** to avoid redundant translations.

---

## 🚀 Features
- Translate text from **English** to **Hindi** or **Korean**.
- Uses **Facebook MBART** (`facebook/mbart-large-50-many-to-many-mmt`).
- Caches translations in **MongoDB** for efficiency.
- Simple **Streamlit UI** for easy interaction.
- **FastAPI** handles requests efficiently.

---

## 🛠️ Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.9.5
- MongoDB (for caching translations)

## Create and Activate a Virtual Environment(for windows)

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

#### 🔧 Install Dependencies 
- Create a **requirements.txt** file,Ensure the  file contains the following dependencies:

- **`fastapi`**: Web framework for building APIs.
- **`uvicorn`**: ASGI server to serve FastAPI.
- **`transformers`**: Hugging Face library for NLP models.
- **`pydantic`**: Data validation for FastAPI requests.
- **`torch`**: Deep learning framework for running ML models.
- **`sentencepiece`**: Tokenizer used in NLP models.
- **`streamlit`**: Frontend framework for creating web apps.
- **`pymongo`**: MongoDB client for database interaction.

- run this to install all the libraries stored in **requirements.txt** file
```bash
pip install -r requirements.txt
```
