import React, {useState} from 'react';
import FacebookLogin from 'react-facebook-login';
import {Navigate} from 'react-router-dom';
import './css/FacebookLoginComponent.css';
import { useUser } from './UserContext';

const FacebookLoginComponent = () => {
    const [redirectToSecurePage, setRedirectToSecurePage] = useState(false);

    const { setUser } = useUser();

    const responseFacebook = (response) => {

        fetch('https://api.teusaquillotimetraveler.online/user/auth/facebook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({response}),
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
        <div className="facebook-login-component">
            <div className="icon-container">
                <img src="/facebook.svg" alt={""}/>
            </div>
            <FacebookLogin
                appId="577978460649702"
                autoLoad={false}
                fields="name,email,picture"
                callback={responseFacebook}
                cssClass="facebook-login-button"
            />
            {redirectToSecurePage && <Navigate to="/user"/>}
        </div>
    );
};

export default FacebookLoginComponent;