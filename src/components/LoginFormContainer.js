import React, { useState } from 'react';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import ErrorPopup from './ErrorPopup';
import axios from 'axios';
import { Navigate } from 'react-router-dom';
import './css/LoginForm.css';
import { useUser } from './UserContext';

const apiUrl = process.env.REACT_APP_API_URL;

const LoginFormContainer = () => {
  const [showSignup, setShowSignup] = useState(false);
  const [redirectToSecurePage, setRedirectToSecurePage] = useState(false);
  const [errorModalOpen, setErrorModalOpen] = useState(false);
  const [modalErrorMessage, setModalErrorMessage] = useState('');

  const { setUser } = useUser();

  const toggleForm = () => {
    setShowSignup(!showSignup);
  };

  const handleLogin = (data) => {
    axios
      .post(apiUrl + '/user/auth/login', data)
      .then((response) => {
        console.log(response.data);
        setUser(response.data);
        setRedirectToSecurePage(true);
      })
      .catch((error) => {
        if (error.response) {
          if (error.response.status === 404) {
            setModalErrorMessage('Please create an account, as it doesn\'t exist.');
          } else if (error.response.status === 401) {
            setModalErrorMessage('Unauthorized. Check your credentials.');
          } else {
            setModalErrorMessage('An error occurred. Please try again.');
          }
        } else if (error.request) {
          setModalErrorMessage('No response from the server. Please try again.');
        } else {
          setModalErrorMessage('An error occurred. Please try again.');
        }

        setErrorModalOpen(true);
      });
  };

  const closeErrorModal = () => {
    setErrorModalOpen(false);
  };

  const handleSignup = async (formData) => {
    if (formData.password !== formData.confirmPassword) {
      console.log('Error with pass');
      return;
    }
    try {
      const response = await axios.post(apiUrl + '/user/auth/signup', formData);
      console.log(response.data);
      setUser(response.data);
      setRedirectToSecurePage(true);
    } catch (error) {
      if (error.response) {
        if (error.response.status === 409) {
          setModalErrorMessage('This email is already in use for an account.');
        } else if (error.response.status === 401) {
          setModalErrorMessage('Unauthorized. Check your credentials.');
        } else {
          setModalErrorMessage('An error occurred. Please try again.');
        }
      } else if (error.request) {
        setModalErrorMessage('No response from the server. Please try again.');
      } else {
        setModalErrorMessage('An error occurred. Please try again.');
      }

      setErrorModalOpen(true);
    }
  };

  return (
    <div className={`container forms${showSignup ? ' show-signup' : ''}`}>
      <ErrorPopup
        isOpen={errorModalOpen}
        onRequestClose={closeErrorModal}
        errorMessage={modalErrorMessage}
      />
      {showSignup ? (
        <SignupForm onToggleLogin={toggleForm} onSignup={handleSignup} />
      ) : (
        <LoginForm onToggleSignup={toggleForm} onLogin={handleLogin} />
      )}
      {redirectToSecurePage && <Navigate to="/user" />}
    </div>
  );
};

export default LoginFormContainer;