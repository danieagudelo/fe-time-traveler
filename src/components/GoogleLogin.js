import React, {useState} from 'react';
import {GoogleOAuthProvider, GoogleLogin} from '@react-oauth/google';
import {Navigate} from 'react-router-dom';
import './css/GoogleLoginComponent.css';
import { useUser } from './UserContext';

const GoogleLoginComponent = () => {

    const [redirectToSecurePage, setRedirectToSecurePage] = useState(false);

    const { setUser } = useUser();

    const responseGoogle = (response) => {
        console.log(response);
        fetch('https://api.teusaquillotimetraveler.online/user/auth/google?token=' + response.credential, {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data && data.token) {
                    console.log(data);
                    setUser(data)
                    setRedirectToSecurePage(true);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    return (
        <div className="google-login-component">
            <GoogleOAuthProvider clientId="214220334130-6dsm28felqurhd2fg2htqcckn02ipk78.apps.googleusercontent.com">
                <div className="google-login-button">
                    <GoogleLogin
                        onSuccess={responseGoogle}
                        onError={() => {
                            console.log('Login Failed');
                        }}
                        className="google-login-button"
                    />
                </div>
            </GoogleOAuthProvider>
            {redirectToSecurePage && <Navigate to="/user"/>}
        </div>
    );
};

export default GoogleLoginComponent;