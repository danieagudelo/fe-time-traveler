import React from 'react';
import {createRoot} from 'react-dom/client'; // Import createRoot from 'react-dom/client' package
import App from './App';
import reportWebVitals from './reportWebVitals';
import {UserProvider} from './components/UserContext';

const root = createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <UserProvider>
            <App/>
        </UserProvider>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();