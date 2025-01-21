import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      setError('');
      const response = await axios.post('http://localhost:5000/extract', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setFormData({
          name: response.data.data.name,
          phone: response.data.data.phone,
          address: response.data.data.address
        });
      } else {
        setError(response.data.error || 'Failed to extract data');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Server Error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Document Information Extractor</h2>
      <div className="upload-section">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileUpload}
          disabled={loading}
        />
        {loading && <p>Processing PDF...</p>}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="form-fields">
        <label>
          Name:
          <input
            type="text"
            value={formData.name}
            readOnly
          />
        </label>

        <label>
          Phone:
          <input
            type="tel"
            value={formData.phone}
            readOnly
          />
        </label>

        <label>
          Address:
          <textarea
            value={formData.address}
            readOnly
          />
        </label>
      </div>
    </div>
  );
};

export default UploadForm;