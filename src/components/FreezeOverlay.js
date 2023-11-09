import React from 'react';

const FreezeOverlay = () => {
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'transparent',
        zIndex: 999,
      }}
    />
  );
};

export default FreezeOverlay;