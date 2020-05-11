import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { AuthNavigator } from './auth.navigator';

const Stack = createStackNavigator();

export const AppNavigator = () => (
  <Stack.Navigator headerMode='none'>
    <Stack.Screen name="Auth" component={AuthNavigator}/>
  </Stack.Navigator>
);