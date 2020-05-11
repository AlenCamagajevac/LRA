import React from 'react';
import { ImageBackground, StyleSheet } from 'react-native';
import { Drawer } from '@ui-kitten/components';

const DrawerHeader = () => (
  <ImageBackground
    style={styles.header}
    source={require('../../assets/image-background.jpeg')}
  />
);

export const HomeDrawer = (props) => {

  const onMenuItemSelect = (index) => {
    const selectedTabRoute = props.state.routeNames[index];
    props.navigation.navigate(selectedTabRoute);
    props.navigation.closeDrawer();
  };

  const createNavigationItemForRoute = (route) => {
    const { options } = props.descriptors[route.key];
    return {
      routeName: route.name,
      title: options.title,
      icon: options.drawerIcon,
    };
  };

  return (
    <Drawer
      header={DrawerHeader}
      data={props.state.routes.map(createNavigationItemForRoute)}
      onSelect={onMenuItemSelect}
    />
  );
};

const styles = StyleSheet.create({
  header: {
    height: 160,
  },
});
