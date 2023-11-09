import React from 'react';

const StarRating = ({ rating }) => {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    const className = i <= rating ? 'star filled' : 'star';
    stars.push(<span key={i} className={className}>&#9733;</span>);
  }

  return <div className="star-rating">{stars}</div>;
};

export default StarRating;