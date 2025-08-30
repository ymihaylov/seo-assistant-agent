import React from 'react';

const DeleteConfirmModal = ({ session, onConfirm, onCancel }) => {
  if (!session) return null;

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Delete Session</h3>
        </div>
        <div className="modal-body">
          <p>
            Are you sure you want to delete the session{' '}
            <strong>"{session.title || 'Unknown'}"</strong>?
          </p>
          <p className="modal-warning">This action cannot be undone.</p>
        </div>
        <div className="modal-actions">
          <button
            className="modal-btn cancel-btn"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button
            className="modal-btn delete-btn"
            onClick={() => onConfirm(session.id)}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;
