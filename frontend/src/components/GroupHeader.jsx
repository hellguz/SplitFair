// ./frontend/src/components/GroupHeader.jsx
/**
 * @file Component to display group information and invite QR code.
 */
import React, { useState } from 'react';
import QRCodeModal from './QRCodeModal';

function GroupHeader({ group }) {
  const [isQRModalOpen, setIsQRModalOpen] = useState(false);
  const inviteLink = `${window.location.origin}/join/${group.invite_code}`;

  return (
    <div style={{ marginBottom: '2rem' }}>
      <h2>{group.name}</h2>
      <div>
        <strong>Members:</strong> {group.users.map(u => u.display_name).join(', ')}
      </div>
      <button onClick={() => setIsQRModalOpen(true)} style={{marginTop: '1rem'}}>
        Invite Others
      </button>
      {isQRModalOpen && (
        <QRCodeModal inviteLink={inviteLink} onClose={() => setIsQRModalOpen(false)} />
      )}
    </div>
  );
}

export default GroupHeader;


