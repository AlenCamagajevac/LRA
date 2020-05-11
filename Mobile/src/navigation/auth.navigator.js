import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { LogInScreen } from '../scenes/auth/LogInScreen';
import 

const Stack = createStackNavigator();

export const AuthNavigator = () => (
  <Stack.Navigator headerMode='none'>
    <Stack.Screen name="LogIn" component={LogInScreen}/>
    <Stack.Screen name="SignUp" component={SignUpScreen}/>
    <Stack.Screen name="ResetPassword" component={ResetPasswordScreen}/>
  </Stack.Navigator>
);