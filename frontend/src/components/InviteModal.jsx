import React from 'react';
import QRCode from 'qrcode.react';

/**
 * A modal that displays the group invite link and a QR code.
 * @param {object} props - The component props.
 * @param {string} props.inviteCode - The unique invite code for the group.
 * @param {Function} props.onClose - Callback function to close the modal.
 * @returns {JSX.Element} The rendered invite modal component.
 */
function InviteModal({ inviteCode, onClose }) {
  const inviteLink = `${window.location.origin}/join/${inviteCode}`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(inviteLink).then(() => {
      alert('Invite link copied to clipboard!');
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Invite friends to your group!</h2>
        <p>Share this link or let them scan the QR code.</p>
        <div className="qr-code">
          <QRCode value={inviteLink} size={256} />
        </div>
        <div className="form-group">
            <input type="text" value={inviteLink} readOnly />
            <button onClick={copyToClipboard} style={{marginTop: "10px"}}>Copy Link</button>
        </div>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default InviteModal;

