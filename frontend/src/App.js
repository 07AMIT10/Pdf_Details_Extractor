// frontend/src/App.js
import React from 'react';
import UploadForm from './components/UploadForm';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>PDF Data Extractor</h1>
            </header>
            <main>
                <UploadForm />
            </main>
            <footer>
                <p>Upload a PDF to automatically extract contact information</p>
            </footer>
        </div>
    );
}

export default App;