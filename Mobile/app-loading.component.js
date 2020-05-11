import React from 'react';
import { AppLoading as ExpoAppLoading, SplashScreen } from 'expo';
import * as Font from 'expo-font';
import { Asset } from 'expo-asset';

export const LoadFontsTask = (fonts) => {
  return Font.loadAsync(fonts).then(() => {return null});
};

export const LoadAssetsTask = (assets) => {
  const tasks = assets.map((source) => {
    return Asset.fromModule(source).downloadAsync();
  });

  return Promise.all(tasks).then(() => null);
};

/*
 * Prevent splash screen from hiding since it is controllable by AppLoading component.
 */
SplashScreen.preventAutoHide();

/**
 * Loads application configuration and returns content of the application when done.
 *
 * @property {Task[]} tasks - Array of tasks to prepare application before it's loaded.
 * A single task should return a Promise with value and a by which this value is accessible.
 *
 * @property {any} fallback - Fallback configuration that is used as default application configuration.
 * May be useful at first run.
 *
 * @property {(props: { loaded: boolean }) => React.ReactElement} placeholder - Element to render
 * while application is loading.
 *
 * @property {(result: any) => React.ReactElement} children - Should return Application component
 */
export const AppLoading = (props) => {

  const [loading, setLoading] = React.useState(true);
  const loadingResult = props.initialConfig || {};

  const onTasksFinish = () => {
    setLoading(false);
    SplashScreen.hide();
  };

  const saveTaskResult = (result) => {
    if (result) {
      loadingResult[result[0]] = result[1];
    }
  };

  const createRunnableTask = (task) => {
    return task().then(saveTaskResult);
  };

  const startTasks = () => {
    if (props.tasks) {
      return Promise.all(props.tasks.map(createRunnableTask));
    }
    return Promise.resolve();
  };

  const renderLoadingElement = () => (
    <ExpoAppLoading
      startAsync={startTasks}
      onFinish={onTasksFinish}
      autoHideSplash={false}
    />
  );

  return (
    <React.Fragment>
      {loading ? renderLoadingElement() : props.children(loadingResult)}
      
    </React.Fragment>
  );
};