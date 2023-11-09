import React from 'react';
import Modal from 'react-modal';
import './css/ErrorPopup.css';


const ErrorPopup = ({ isOpen, onRequestClose, errorMessage }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      contentLabel="Error Popup"
      className="custom-modal-content"
    >
      <div className="error-popup">
         <img className="warning-popup" src="/warning.png"  alt={""}/>
        <div className="field">
          <p className="error-message-popup">{errorMessage}</p>
        </div>
        <div className="field button-field">
          <button className="error-popup-button" onClick={onRequestClose}>
            Close
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default ErrorPopup;
