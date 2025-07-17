import React, { useState } from 'react';
import InviteModal from './InviteModal';

/**
 * Displays the header for a group page, including the group name and an invite button.
 * @param {object} props - The component props.
 * @param {string} props.name - The name of the group.
 * @param {string} props.inviteCode - The unique invite code for the group.
 * @returns {JSX.Element} The rendered group header component.
 */
function GroupHeader({ name, inviteCode }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>{name}</h2>
        <button onClick={() => setIsModalOpen(true)}>Invite Friends</button>
      </div>
      {isModalOpen && (
        <InviteModal
          inviteCode={inviteCode}
          onClose={() => setIsModalOpen(false)}
        />
      )}
    </>
  );
}

export default GroupHeader;

