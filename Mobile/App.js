import React from 'react';
import { StyleSheet } from 'react-native';
import { ApplicationProvider } from '@ui-kitten/components';
import { mapping, light as lightTheme } from '@eva-design/eva';
import NewsScreen  from './src/screens/NewsScreen'

export default function App() {
  return (
    <ApplicationProvider mapping={mapping} theme={lightTheme}> 
      <NewsScreen></NewsScreen>
    </ApplicationProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
