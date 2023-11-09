import React, {useState, useEffect, useRef} from 'react';
import GoogleMapReact from 'google-map-react';
import StarRating from './StarRating';
import './css/GoogleMap.css';
import './css/CommentSection.css';
import {useUser} from './UserContext';
import {jwtDecode} from "jwt-decode";


const apiUrl = process.env.REACT_APP_API_URL;

const AnyReactComponent = ({text, onClick, id}) => (
    <div style={{position: 'relative'}}>
        <img
            src="/pin.png"
            alt=""
            className="custom-marker"
            onClick={() => onClick(id)}
        />
        {text}
    </div>
);

const getRelativeTime = (timestamp) => {
    const currentDate = new Date();
    const commentDate = new Date(timestamp);
    const timeDifference = currentDate - commentDate;
    const seconds = Math.floor(timeDifference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const months = Math.floor(days / 30);
    const years = Math.floor(months / 12);

    if (years > 0) {
        return `${years} ${years === 1 ? 'year' : 'years'} ago`;
    } else if (months > 0) {
        return `${months} ${months === 1 ? 'month' : 'months'} ago`;
    } else if (days > 0) {
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
    } else if (hours > 0) {
        return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
    } else if (minutes > 0) {
        return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;
    } else {
        return `${seconds} ${seconds === 1 ? 'second' : 'seconds'} ago`;
    }
};

const GoogleMap = () => {
    const [rating] = useState(4.5);
    const [markers, setMarkers] = useState([]);
    const [selectedMarker, setSelectedMarker] = useState(null);
    const [selectedText, setSelectedText] = useState('');
    const [selectedTitle, setSelectedTitle] = useState('');
    const [selectedImages, setSelectedImages] = useState([]);
    const [imageIndex, setImageIndex] = useState(0);
    const [comments, setComments] = useState([]);
    const [comment, setComment] = useState('');

    const mapContainerRef = useRef(null);

    const {user} = useUser();

    useEffect(() => {
        fetch(apiUrl+'/locations')
            .then((response) => response.json())
            .then((data) => {
                // Parse lat and lng to floats
                const parsedData = data.map((marker) => ({
                    ...marker,
                    lat: parseFloat(marker.lat),
                    lng: parseFloat(marker.lng),
                }));
                setMarkers(parsedData);
            })
            .catch((error) => {
                console.error('Error fetching marker data:', error);
            });
    }, []);

    useEffect(() => {
        if (user) {
            console.log('User Data:', user);
        }
    }, [user]);


    const fetchComments = (locationId) => {
        fetch(apiUrl+`/comments?location_id=${locationId}`)
            .then((response) => response.json())
            .then((data) => setComments(data))
            .catch((error) => {
                console.error('Error fetching comments:', error);
            });
    };

    const handleSubmitComment = async () => {
        if (comment.trim() === '') {
            return;
        }

        const locationId = selectedMarker;

        const token = user ? user.token : null;
        const userId = token ? jwtDecode(token)?.sub : null;
        const username = token ? jwtDecode(token)?.name : "Guest";


        const timestamp = new Date().toISOString();


        const commentData = {
            location_id: locationId,
            user_id: userId,
            username: username,
            text: comment,
            created: timestamp,
        };

        console.log(commentData)
        setComments([...comments, commentData]);
        setComment('');


        try {
            const response = await fetch(apiUrl+'/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(commentData),
            });

            if (!response.ok) {
                throw new Error(`Failed to submit comment - Status: ${response.status}`);
            }

            const data = await response.json();
            setComments([data, ...comments]);
            setComment('');
        } catch (error) {
            console.error('Error submitting comment:', error);
        }
    };


    const defaultProps = {
        center: {
            lat: 4.624474886090981,
            lng: -74.07290498520929,
        },
        zoom: 16.5,
        draggable: false,
    };

    const handleMarkerClick = (markerId) => {
        const selectedMarkerData = markers.find((marker) => marker.id === markerId);
        if (selectedMarkerData) {
            setSelectedMarker(markerId);
            setSelectedTitle(selectedMarkerData.title);
            setSelectedText(selectedMarkerData.text);
            setSelectedImages(selectedMarkerData.images);
            setImageIndex(0);

            fetchComments(markerId);
        }
    };

    const handleMapClick = (e) => {
        if (
            mapContainerRef.current &&
            !mapContainerRef.current.contains(e.target)
        ) {
            setSelectedMarker(null);
            document.body.style.overflow = 'visible';
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Escape') {
            setSelectedMarker(null);
            document.body.style.overflow = 'visible';
        }
    };

    useEffect(() => {
        document.body.style.overflow = selectedMarker !== null ? 'hidden' : 'visible';
        window.addEventListener('keydown', handleKeyDown);

        return () => {
            document.body.style.overflow = 'visible';
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [selectedMarker]);

    const handleImagePrev = () => {
        setImageIndex(
            (prevIndex) => (prevIndex - 1 + selectedImages.length) % selectedImages.length
        );
    };

    const handleImageNext = () => {
        setImageIndex(
            (prevIndex) => (prevIndex + 1) % selectedImages.length
        );
    };


    const handleLike = async (commentId) => {
        try {
            const updatedComment = await reactToComment(commentId, 'like');
            setComments((prevComments) =>
                prevComments.map((comment) =>
                    comment.id === commentId ? updatedComment : comment
                )
            );
        } catch (error) {
            console.error('Error reacting to comment:', error);
        }
    };

    const handleDislike = async (commentId) => {
        try {
            const updatedComment = await reactToComment(commentId, 'dislike');
            setComments((prevComments) =>
                prevComments.map((comment) =>
                    comment.id === commentId ? updatedComment : comment
                )
            );
        } catch (error) {
            console.error('Error reacting to comment:', error);
        }
    };

    const reactToComment = async (commentId, reactionType) => {
        try {
            const token = user ? user.token : null;
            const userId = token ? jwtDecode(token)?.sub : null;

            const response = await fetch(apiUrl+'/comments/react', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    comment_id: commentId,
                    reaction_type: reactionType,
                    user_id: userId,
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed to react to comment - Status: ${response.status}`);
            }

            const updatedComment = await response.json();
            return updatedComment;

        } catch (error) {
            console.error('Error reacting to comment:', error);
        }
    };

    return (
        <div className="map-container" ref={mapContainerRef} onClick={handleMapClick}>
            <GoogleMapReact
                bootstrapURLKeys={{
                    key: 'AIzaSyBoEQde7SsgSK7o3C89akbT1Z6dDl2T6nA',
                }}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}
                draggable={defaultProps.draggable}
            >
                {markers.map((marker) => (
                    <AnyReactComponent
                        key={marker.id}
                        lat={marker.lat}
                        lng={marker.lng}
                        id={marker.id}
                        onClick={handleMarkerClick}
                    />
                ))}
            </GoogleMapReact>

            {selectedMarker !== null && (
                <div className="banner">

                    <h2 className="banner-title">{selectedTitle}</h2>
                    <StarRating rating={rating}/>


                    <div className="image-slider">
                        <div className="image-container">
                            {/* eslint-disable-next-line jsx-a11y/img-redundant-alt */}
                            <img src={selectedImages[imageIndex]} alt="Image"/>
                        </div>
                    </div>
                    <div className="image-slider-container">
                        <div className="image-slider-icon">
                            <img
                                src="/before.png"
                                alt="Previous"
                                onClick={handleImagePrev}
                                className="slider-icon"
                            />
                            <img
                                src="/next.png"
                                alt="Next"
                                onClick={handleImageNext}
                                className="slider-icon"
                            />
                        </div>
                    </div>

                    <div className="description">
                        <p>
                            {selectedText}
                        </p>
                    </div>

                    <div className="comments">
                        <div className="comment-scroll">
                            {comments.map((comment) => (
                                <div className="media" key={comment.id}>
                                    <div className="user-avatar">
                                        <div className="avatar">
                                            {comment.username ? comment.username.substring(0, 2).toUpperCase() : ''}
                                        </div>
                                    </div>
                                    <div className="comment-content">
                                        <div className="comment-header">
                                            <h5 className="comment-username">{comment.username}</h5>
                                            <span
                                                className="comment-timestamp">{getRelativeTime(comment.created)}</span>
                                        </div>
                                        <p className="comment-text">{comment.text}</p>
                                        <ul className="comment-actions">
                                            <li className="comment-action">
                                                <a href="#!" onClick={() => handleLike(comment.id)}>
                                                    <i className="fa fa-thumbs-up"></i> {comment.likes}
                                                </a>
                                            </li>
                                            <li className="comment-action">
                                                <a href="#!" onClick={() => handleDislike(comment.id)}>
                                                    <i className="fa fa-thumbs-down"></i> {comment.dislikes}
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="comment-input-container">
                            <input
                                type="text"
                                className="comment-input"
                                placeholder="Add a comment"
                                value={comment}
                                onChange={(e) => setComment(e.target.value)}
                            />
                            <button className="comment-submit-button" onClick={handleSubmitComment}>
                                <i className="fa fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GoogleMap;
