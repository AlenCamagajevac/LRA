import React from 'react';
import {
  OverflowMenu,
  TopNavigation,
  TopNavigationAction
} from '@ui-kitten/components';
import { BackIcon, MoreVerticalIcon } from '../../assets/icons';


export const Toolbar = (props) => {

  const { menu, backIcon, menuIcon, onMenuItemSelect, onBackPress, ...topNavigationProps } = props;
  const [menuVisible, setMenuVisible] = React.useState(false);

  const onMenuSelect = (index) => {
    setMenuVisible(false);
    onMenuItemSelect && onMenuItemSelect(index);
  };

  const onMenuActionPress = () => {
    setMenuVisible(!menuVisible);
  };

  const renderMenuAction = (menu) => (
    <OverflowMenu
      visible={menuVisible}
      data={menu}
      placement='bottom end'
      onSelect={onMenuSelect}
      onBackdropPress={onMenuActionPress}>
      <TopNavigationAction
        icon={props.menuIcon || MoreVerticalIcon}
        onPress={onMenuActionPress}
      />
    </OverflowMenu>
  );

  const renderBackAction = () => (
    <TopNavigationAction
      icon={props.backIcon || BackIcon}
      onPress={onBackPress}
    />
  );

  return (
    <React.Fragment>
      <TopNavigation
        {...topNavigationProps}
        alignment='center'
        leftControl={onBackPress && renderBackAction()}
        rightControls={menu && renderMenuAction(menu)}
      />
    </React.Fragment>
  );
};
