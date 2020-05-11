import React from 'react';
import { ApplicationProvider, IconRegistry } from '@ui-kitten/components';
import { EvaIconsPack } from '@ui-kitten/eva-icons';
import LoginScreen from './src/scenes/auth/LogInScreen';
import RegisterScreen from './src/scenes/auth/RegisterScreen';
import NewsScreen from './src/screens/NewsScreen';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import { Provider as AuthProvider } from './src/context/AuthContext';
import { Provider as ArticleProvider } from './src/context/ArticleContext';
import { setNavigator } from './src/NavigationRef';
import { AppLoading, LoadFontsTask, Task } from './app-loading.component';
import { appMappings, appThemes } from './app-theming';
import { Theming } from './src/services/theme.service';
import { AppearanceProvider } from 'react-native-appearance';
import { SplashImage } from './src/components/splash-image.component';
import { AppStorage } from './src/services/app-storage.service';
import AppNavigator  from './src/screens/IndexScreen';

const loadingTasks = [
  // Should be used it when running Expo.
  () => LoadFontsTask({
    'OpenSans-Regular': require('./assets/fonts/OpenSans-Regular.ttf'),
    'OpenSans-SemiBold': require('./assets/fonts/OpenSans-SemiBold.ttf'),
    'OpenSans-Bold': require('./assets/fonts/OpenSans-Bold.ttf'),
    'Roboto-Regular': require('./assets/fonts/Roboto-Regular.ttf'),
    'Roboto-Medium': require('./assets/fonts/Roboto-Medium.ttf'),
    'Roboto-Bold': require('./assets/fonts/Roboto-Bold.ttf'),
  }),
  () => AppStorage.getMapping(defaultConfig.mapping).then(result => ['mapping', result]),
  () => AppStorage.getTheme(defaultConfig.theme).then(result => ['theme', result]),
];

const defaultConfig = {
  mapping: 'eva',
  theme: 'light',
};

const navigatorConfig = createStackNavigator(
  {
    NewsScreen: NewsScreen,
    LoginScreen: LoginScreen,
    RegisterScreen: RegisterScreen
  },
  {
    initialRouteName: 'IndexScreen',
    defaultNavigationOptions: {
      headerShown: false
    }
  }
);



const App = ({mapping, theme}) => {

  const Navigator = createAppContainer(navigatorConfig);

  const [mappingContext, currentMapping] = Theming.useMapping(appMappings, mapping);
  const [themeContext, currentTheme] = Theming.useTheming(appThemes, mapping, theme);

  return(
  <React.Fragment>
    <IconRegistry icons={EvaIconsPack} />
    <AppearanceProvider>
      <ApplicationProvider {...currentMapping} theme={currentTheme}>
      <Theming.MappingContext.Provider value={mappingContext}>
      <Theming.ThemeContext.Provider value={themeContext}>
        <ArticleProvider>
          <AuthProvider>
            <AppNavigator></AppNavigator>
          </AuthProvider>
        </ArticleProvider>
        </Theming.ThemeContext.Provider>
        </Theming.MappingContext.Provider>
      </ApplicationProvider>
    </AppearanceProvider>
  </React.Fragment>
  );
};

const Splash = ({ loading })=> (
  <SplashImage
    loading={loading}
    source={require('./assets/images/image-splash.png')}
  />
);

export default () => (
  <AppLoading
    tasks={loadingTasks}
    initialConfig={defaultConfig}
    //placeholder={Splash}
    >
    {props => <App {...props}/>}
  </AppLoading>
);