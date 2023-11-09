import React, {useRef, useState} from 'react';
import FacebookLogin from './FacebookLogin';
import GoogleLogin from './GoogleLogin';
import './css/LoginForm.css';

const LoginForm = ({onToggleSignup, onLogin, onGoogleLogin, onFacebookLogin}) => {
    const emailRef = useRef();
    const passwordRef = useRef();
    const [error, setError] = useState('');

    const isEmailValid = (email) => {
        const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        return emailRegex.test(email);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const email = emailRef.current.value;
        const password = passwordRef.current.value;

        if (!email || !password) {
            setError('All fields are required');
        } else if (!isEmailValid(email)) {
            setError('Invalid email format');
        } else {
            setError('');
            onLogin({email, password});
        }
    };

    return (
        <div className="form login">
            <div className="form-content">
                <header>Login</header>
                <form onSubmit={handleSubmit}>
                    <div className="field input-field">
                        <input type="email" placeholder="Email" className="input" ref={emailRef}/>
                    </div>
                    <div className="field input-field">
                        <input type="password" placeholder="Password" className="password" ref={passwordRef}/>
                        <i className='bx bx-hide eye-icon'></i>
                    </div>
                    <div className="form-link">
            <span>
              Don't have an account?{' '}
                <button onClick={onToggleSignup} className="link signup-link">
                Signup
              </button>
            </span>
                    </div>
                    {error && <p className="error-message">{error}</p>}
                    <div className="field button-field">
                        <button type="submit">Login</button>
                    </div>
                </form>
            </div>
            <div className="line"></div>
            <div>
                <FacebookLogin/>
            </div>
            <div>
                <GoogleLogin/>
            </div>
        </div>
    );
};

export default LoginForm;