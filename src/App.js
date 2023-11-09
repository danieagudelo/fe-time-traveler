import React from 'react';
import './App.css';
import UserPage from "./components/UserPage";
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import LoginFormContainer from './components/LoginFormContainer';

/*<Route path="/" element={<GoogleLogin />} />*/
function App() {
  return (
      <Router>
          <Routes>
              <Route path="/login" element={<LoginFormContainer />} />
              <Route path="/user" element={<UserPage />} />
              {/* You can add more routes as needed */}
          </Routes>
    </Router>
  );
}

export default App;
