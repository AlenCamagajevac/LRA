import React from 'react';
import { ImageBackground, StyleSheet, View } from 'react-native';
import { Avatar, Button, Card, Layout, List, Text } from '@ui-kitten/components';
import { HeartIcon, MessageCircleIcon } from '../components/icons/icons';
import { Article, Profile, Comment, Like } from './test/data';

const data = [
    Article.howToEatHealthy(),
    Article.morningWorkouts(),
    Article.whyWorkoutImportant(),
  ];

const NewsScreen = () => {

  const onItemPress = (index) => { };

  const renderItemHeader = (info) => (
    <ImageBackground
      style={styles.itemHeader}
      source={info.item.image}
    />
  );

  const renderItemFooter = (info) => (
    <View style={styles.itemFooter}>
      <Avatar source={info.item.author.photo}/>
      <View style={styles.itemAuthoringContainer}>
        <Text
          category='s2'>
          {info.item.author.fullName}
        </Text>
        <Text
          appearance='hint'
          category='c1'>
          {info.item.date}
        </Text>
      </View>
      <Button
        style={styles.iconButton}
        appearance='ghost'
        status='basic'
        icon={MessageCircleIcon}>
        {`${info.item.comments.length}`}
      </Button>
      <Button
        style={styles.iconButton}
        appearance='ghost'
        status='danger'
        icon={HeartIcon}>
        {`${info.item.likes.length}`}
      </Button>
    </View>
  );

  const renderItem = (info) => {
    let article1 = new Article(
        'How To Eat Healthy',
        '10 useful Tips',
        'There\'s a lot of advice out there on how to eat healthy, and if we\'re being honest, it can sometimes feel like too much to think about. Especially when you\'re hungry. Remember when you were a kid and eating was as simple as open, chew, enjoy? Yes, those were simpler times. Now, knowing how to eat healthy doesn\'t seem quite as straightforward. Between the diet fads, gourmet trends, and a rotating roster of superfoods, eating well has gotten, well, complicated.',
        require('../screens/assets/image-article-background-1.jpg'),
        '19 Sep, 2018',
        Profile.markVolter(),
        [
          Like.byMarkVolter(),
          Like.byHubertFranck(),
        ],
        [
          Comment.byHubertFranck(),
          Comment.byHubertFranck(),
          Comment.byHubertFranck(),
        ],
      );

    console.log("article: ", article1);    

    return (
    <Card
      style={styles.item}
      header={() => renderItemHeader(info)}
      footer={() => renderItemFooter(info)}
      onPress={() => onItemPress(info.index)}>
      <Text category='h5'>
        {info.item.title}
      </Text>
      <Text
        style={styles.itemContent}
        appearance='hint'
        category='s1'>
        {`${info.item.content.substring(0, 82)}...`}
      </Text>
    </Card>
  )};

  return (
    <Layout
      style={styles.container}
      level='2'>
      <List
        style={styles.list}
        contentContainerStyle={styles.listContent}
        data={data}
        renderItem={renderItem}
      />
    </Layout>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  list: {
    flex: 1,
  },
  listContent: {
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  item: {
    marginVertical: 8,
  },
  itemHeader: {
    height: 220,
  },
  itemContent: {
    marginVertical: 8,
  },
  itemFooter: {
    flexDirection: 'row',
    marginHorizontal: -8,
  },
  iconButton: {
    paddingHorizontal: 0,
  },
  itemAuthoringContainer: {
    flex: 1,
    justifyContent: 'center',
    marginHorizontal: 16,
  },
});

export default NewsScreen;