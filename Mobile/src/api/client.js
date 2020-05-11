import axios from 'axios';
import { AsyncStorage } from 'react-native';


let url;
if (__DEV__) {
  url = 'http://192.168.0.29:5000';
} else {
  url = 'https://sleepy-savannah-10606.herokuapp.com';
}

const instance = axios.create({
  baseURL: url
});

instance.interceptors.request.use(
  async config => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
        // Check if token is expiered - if it is fetch the new one
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);

export default instance;