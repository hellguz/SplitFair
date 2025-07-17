// ./frontend/src/components/QRCodeModal.jsx
/**
 * @file Modal component to display a QR code for the group invite link.
 */
import React from 'react';
import QRCode from 'qrcode.react';

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.7)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000,
};

const modalContentStyle = {
  backgroundColor: '#fff',
  color: '#333',
  padding: '20px',
  borderRadius: '8px',
  textAlign: 'center',
  position: 'relative',
};

function QRCodeModal({ inviteLink, onClose }) {
  return (
    <div style={modalOverlayStyle} onClick={onClose}>
      <div style={modalContentStyle} onClick={(e) => e.stopPropagation()}>
        <h3>Scan to Join Group</h3>
        <QRCode value={inviteLink} size={256} />
        <p>Or share this link:</p>
        <input type="text" readOnly value={inviteLink} style={{width: '90%'}}/>
        <br/>
        <button onClick={onClose} style={{marginTop: '1rem'}}>Close</button>
      </div>
    </div>
  );
}

export default QRCodeModal;

