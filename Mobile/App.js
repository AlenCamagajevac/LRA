import React from 'react';
import { ApplicationProvider, IconRegistry, Layout, Text } from '@ui-kitten/components';
import { EvaIconsPack } from '@ui-kitten/eva-icons';
import { mapping, light as lightTheme } from '@eva-design/eva';
import LoginScreen  from './src/screens/LoginScreen';

// export default function App() {
//   return (
//     <ApplicationProvider {...eva} theme={eva.light}> 
//       <LoginScreen></LoginScreen>
//     </ApplicationProvider>
//   );
// }

const App = () => (
  <React.Fragment>
    <IconRegistry icons={EvaIconsPack} />
    <ApplicationProvider mapping={mapping} theme={lightTheme}>
      <LoginScreen />
    </ApplicationProvider>
  </React.Fragment>
);

export default App;