import React from 'react';
import { ApplicationProvider, IconRegistry } from '@ui-kitten/components';
import { EvaIconsPack } from '@ui-kitten/eva-icons';
import { mapping, light as lightTheme } from '@eva-design/eva';
import LoginScreen  from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import NewsScreen from './src/screens/NewsScreen';
import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import { Provider as AuthProvider } from './src/context/AuthContext';

const navigator = createStackNavigator(
  {
    NewsScreen: NewsScreen,
    LoginScreen: LoginScreen,
    RegisterScreen: RegisterScreen
  },
  {
    initialRouteName: 'LoginScreen',
    defaultNavigationOptions: {
      headerShown: false
    }
  }
);

const App = createAppContainer(navigator);

export default () => (
  <React.Fragment>
    <IconRegistry icons={EvaIconsPack} />
    <ApplicationProvider mapping={mapping} theme={lightTheme}>
      <AuthProvider>
        <App />
      </AuthProvider>
    </ApplicationProvider>
  </React.Fragment>
);