import React, { createContext, useContext, useReducer } from 'react';

const initialUserState = {
  user: null,
};

const UserContext = createContext();

export const useUser = () => {
  return useContext(UserContext);
};

const SET_USER = 'SET_USER';

const userReducer = (state, action) => {
  switch (action.type) {
    case SET_USER:
      return { ...state, user: action.payload };
    default:
      return state;
  }
};

export const UserProvider = ({ children }) => {
  const [state, dispatch] = useReducer(userReducer, initialUserState);

  const setUser = (user) => {
    dispatch({ type: SET_USER, payload: user });
  };

  return (
    <UserContext.Provider value={{ user: state.user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};