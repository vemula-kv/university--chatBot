# University Hybrid Chatbot

This is a hybrid chatbot that combines **Button Navigation** with **Azure OpenAI RAG** (Retrieval Augmented Generation).

## 📂 Project Structure
- `backend/`: FastAPI Python server + Mock Data + AI Logic.
- `frontend/`: Custom HTML/JS Chat Interface.

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.8+ installed.
- VS Code or Terminal.
- An Azure OpenAI API Key and Endpoint.

### 2. Backend Setup
1. Open your terminal and navigate to the `backend` folder:
   ```powershell
   cd backend
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure Azure Keys**:
   - Create a file named `.env` inside the `backend` folder.
   - Add your keys like this:
     ```
     AZURE_OPENAI_API_KEY=your_key_here
     AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
     AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
     AZURE_OPENAI_API_VERSION=2023-05-15
     ```

4. Start the Server:
   ```powershell
   python app.py
   ```
   *The server will start at `http://127.0.0.1:8001`*

### 3. Frontend Setup
1. **Easiest Way**:
   Open `http://localhost:8001` in your browser. The server now hosts the frontend directly!

2. **Old Way**:
   Go to the `frontend` folder and open `index.html` manually.

## 🤖 Features
- **Button Flow**: Navigate via categories (Admissions, Courses, etc.).
- **AI Query**: Click "Ask a Question" or type freely. The bot will search its internal `mock_data.json` and use Azure OpenAI to answer.
- **RAG**: The bot reads from the `mock_data.json` file to provide accurate university info.

## 📝 Customization
- **Data**: Edit `backend/mock_data.json` to change the university information.
- **Styles**: Edit `frontend/styles.css` to change colors and branding.
