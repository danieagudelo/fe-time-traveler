import React from 'react';
import './App.css';
import UserPage from "./components/UserPage";
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import LoginFormContainer from './components/LoginFormContainer';

/*<Route path="/" element={<GoogleLogin />} />*/
function App() {
  return (
      <Router>
          <Routes>
              <Route path="/" element={<Navigate to="/login" />} />

              <Route path="/login" element={<LoginFormContainer />} />
              <Route path="/user" element={<UserPage />} />
          </Routes>
    </Router>
  );
}

export default App;
