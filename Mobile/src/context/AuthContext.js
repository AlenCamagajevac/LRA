import { AsyncStorage } from 'react-native';
import createDataContext from './CreateDataContext';
import client from '../api/client';
import { navigate } from '../NavigationRef';

var jwtDecode = require('jwt-decode');

const authReducer = (state, action) => {
    switch (action.type) {
        case 'add_error':
            return { ...state, errorMessage: action.payload };
        case 'signin':
            return {
                errorMessage: '',
                user: action.payload
            };
        case 'clear_error_message':
            return { ...state, errorMessage: '' };
        case 'signout':
            return { token: null, errorMessage: '' };
        default:
            return state;
    }
};

const clearErrorMessage = dispatch => () => {
    dispatch({ type: 'clear_error_message' });
};

const signup = dispatch => async ({ email, password }) => {
    try {
        // Send login request
        const response = await client.post('/api/auth/login', { email, password });
        await AsyncStorage.setItem('access_token', response.data.access_token);
        await AsyncStorage.setItem('refresh_token', response.data.refresh_token);
        var decoded = jwtDecode(token);


        dispatch({ type: 'signin', payload: response.data.token });

        navigate('TrackList');
    } catch (err) {
        console.log(err);
        dispatch({
            type: 'add_error',
            payload: 'Something went wrong with sign up'
        });
    }
};

const signin = dispatch => async ({ email, password }) => {
    try {
        // Send login request   
        const response = await client.post('/api/auth/login', { email, password });

        // Save access and refresh token to storage
        await AsyncStorage.setItem('access_token', response.data.access_token);
        await AsyncStorage.setItem('refresh_token', response.data.refresh_token);

        // Decode token
        var userInfo = jwtDecode(response.data.access_token);
        dispatch({ type: 'signin', payload: userInfo.user_claims });
        navigate('NewsScreen');
    } catch (err) {
        console.log(err.response);
        dispatch({
            type: 'add_error',
            payload: 'Something went wrong with sign in'
        });
    }
};

const signout = dispatch => async () => {
    await AsyncStorage.removeItem('token');
    dispatch({ type: 'signout' });
    navigate('loginFlow');
};

export const { Provider, Context } = createDataContext(
    authReducer,
    { signin, signout, signup, clearErrorMessage },
    { user: null, errorMessage: '' }
);