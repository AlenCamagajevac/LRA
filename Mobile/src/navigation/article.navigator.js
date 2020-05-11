import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { AppRoute } from './app-routes';
import { 
  AllArticlesScreen, 
  ArticleCategoriesScreen, 
  ArticleDetailsScreen, 
  ArticleTabBar
} from '../scenes/article';
import { DoneAllIcon, GridIcon } from '../../assets/icons';


const Stack = createStackNavigator();
const TopTab = createMaterialTopTabNavigator();


const ArticleTabsNavigator = () => (
  <TopTab.Navigator tabBar={props => <ArticleTabBar {...props} />}>
    <TopTab.Screen
      name={AppRoute.ALL_ARTICLES}
      component={AllArticlesScreen}
      options={{ title: 'IN PROGRESS', tabBarIcon: GridIcon }}
    />
    <TopTab.Screen
      name={AppRoute.ARTICLE_CATEGORIES}
      component={ArticleCategoriesScreen}
      options={{ title: 'DONE', tabBarIcon: DoneAllIcon }}
    />
  </TopTab.Navigator>
);

export const ArticleNavigator = () => (
  <Stack.Navigator headerMode='none'>
    <Stack.Screen name={AppRoute.ARTICLE} component={ArticleTabsNavigator}/>
    <Stack.Screen name={AppRoute.ARTICLE_DETAILS} component={ArticleDetailsScreen}/>
  </Stack.Navigator>
);
