import React from 'react';
import { View } from 'react-native';
import { Text, withStyles } from '@ui-kitten/components';


const ProgressBarComponent = ({ progress, text, ...props }) => (
  <View style={props.themedStyle.container}>
    <View
      {...props}
      style={[props.themedStyle.progressContainer, props.style]}>
      <View style={[props.themedStyle.progress, { width: `${progress}%` }]}/>
    </View>
    {text && <Text style={props.themedStyle.text} category='c2'>{text}</Text>}
  </View>
);

export const ProgressBar = withStyles(ProgressBarComponent, (theme) => ({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressContainer: {
    height: 6,
    borderRadius: 3,
    backgroundColor: theme['background-basic-color-2'],
    overflow: 'hidden',
  },
  progress: {
    flex: 1,
    backgroundColor: theme['color-primary-default'],
  },
  text: {
    marginHorizontal: 16,
  },
}));

