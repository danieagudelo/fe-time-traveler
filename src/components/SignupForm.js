import React, {useState} from 'react';
import FacebookLogin from './FacebookLogin';
import GoogleLogin from './GoogleLogin';
import './css/LoginForm.css';

const SignupForm = ({onToggleLogin, onSignup, onGoogleSignup, onFacebookSignup}) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    const [error, setError] = useState('');

    const isEmailValid = (email) => {
        const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        return emailRegex.test(email);
    };

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formData.email || !formData.password || !formData.confirmPassword) {
            setError('All fields are required');
        } else if (!isEmailValid(formData.email)) {
            setError('Invalid email format');
        } else if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
        } else {
            setError('');
            onSignup(formData);
        }
    };

    return (
        <div className="form signup">
            <div className="form-content">
                <header>Signup</header>
                <form onSubmit={handleSubmit}>
                    <div className="field input-field">
                        <input
                            type="name"
                            name="name"
                            placeholder="Name"
                            className="input"
                            value={formData.name}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="field input-field">
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            className="input"
                            value={formData.email}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="field input-field">
                        <input
                            type="password"
                            name="password"
                            placeholder="Create password"
                            className="password"
                            value={formData.password}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="field input-field">
                        <input
                            type="password"
                            name="confirmPassword"
                            placeholder="Confirm password"
                            className="password"
                            value={formData.confirmPassword}
                            onChange={handleInputChange}
                        />
                        <i className='bx bx-hide eye-icon'></i>
                    </div>
                    <div className="form-link">
            <span>
              Already have an account?{' '}
                <button onClick={onToggleLogin} className="link login-link">
                Login
              </button>
            </span>
                    </div>
                    {error && <p className="error-message">{error}</p>}
                    <div className="field button-field">
                        <button type="submit">Signup</button>
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

export default SignupForm;