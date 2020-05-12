import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { light, mapping } from '@eva-design/eva';
import { ApplicationProvider, IconRegistry } from '@ui-kitten/components';
import { EvaIconsPack } from '@ui-kitten/eva-icons';
import { AppNavigator } from './src/navigation/app.navigator';
import { AppRoute } from './src/navigation/app-routes';
import { Provider as ArticleContext } from './src/context/article.context';

export default () => {

  // This value is used to determine the initial screen
  const isAuthorized = false;

  return (
    <React.Fragment>
      <IconRegistry icons={EvaIconsPack} />
      <ApplicationProvider
        mapping={mapping}
        theme={light}>
        <SafeAreaProvider>
          <ArticleContext>
            <NavigationContainer>
              <AppNavigator initialRouteName={isAuthorized ? AppRoute.HOME : AppRoute.AUTH} />
            </NavigationContainer>
          </ArticleContext>
        </SafeAreaProvider>
      </ApplicationProvider>
    </React.Fragment>
  );
};