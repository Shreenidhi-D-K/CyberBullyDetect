import React, { useState } from 'react';

const Home = () => {
    const [text, setText] = useState('');
    const [file, setFile] = useState(null);
    const [classificationResult, setClassificationResult] = useState('');

    const handleTextChange = (e) => {
        setText(e.target.value);
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFile(file);
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('text', text);
    
        const response = await fetch('http://localhost:5000/classify', {
            method: 'POST',
            body: formData
        });
    
        const result = await response.text();
        const parsedResult = JSON.parse(result);
        setClassificationResult(parsedResult.result);

    };

    return (
        <>
            <div style={{ backgroundColor: '#0ff0ff', height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <div style={{ width: '50%', textAlign: 'center' }}>
                    <h1>Cyberbully Detection</h1>

                    <br />
                    <textarea placeholder="Enter text here..." style={{ width: '100%', height: '100px' }} onChange={handleTextChange}></textarea>
                    <br />
                    <button onClick={handleSubmit}>Submit</button>
                    <br />
                    <span style={{ color: 'green' }}>{classificationResult}</span>
                </div>
            </div>
        </>
    );
}

export default Home;
