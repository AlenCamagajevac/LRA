import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { AppRoute } from './app-routes';
import { ProfileScreen } from '../scenes/profile';


const Stack = createStackNavigator();

export const ProfileNavigator = () => (
  <Stack.Navigator headerMode='none'>
    <Stack.Screen name={AppRoute.PROFILE} component={ProfileScreen}/>
  </Stack.Navigator>
);
