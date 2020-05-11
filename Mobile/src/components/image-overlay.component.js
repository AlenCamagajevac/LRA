import React from 'react';
import {
  ImageBackground,
  StyleSheet,
  View
} from 'react-native';


const DEFAULT_OVERLAY_COLOR = 'rgba(0, 0, 0, 0.15)';

export class ImageOverlay extends React.Component {

  render() {
    const { style, children, ...restProps } = this.props;
    const { overlayColor: derivedOverlayColor, ...containerStyle } = StyleSheet.flatten(style);

    const overlayColor = this.getOverlayColor(derivedOverlayColor);

    return (
      <ImageBackground
        style={containerStyle}
        {...restProps}>
        <View style={[styles.overlay, { backgroundColor: overlayColor }]}/>
        {children}
      </ImageBackground>
    );
  }

  getOverlayColor = (source) => {
    return source || DEFAULT_OVERLAY_COLOR;
  };
}

const styles = StyleSheet.create({
  overlay: {
    backgroundColor: DEFAULT_OVERLAY_COLOR,
    ...StyleSheet.absoluteFillObject,
  },
});
