import React, { useContext, useEffect, useState } from 'react';
import { ImageBackground, View } from 'react-native';
import { Button, Card, Layout, List, Text, Spinner, StyleService, useStyleSheet } from '@ui-kitten/components';
import { Context } from '../context/ArticleContext';

export default NewsScreen = ({ navigation }) => {

  const articleListRef = React.useRef()

  const styles = useStyleSheet(themedStyles);

  const { state, getArticles } = useContext(Context);
  const [endReached, setEndReached] = useState(false);


  useEffect(() => {
    getArticles(1, '2020-04-28', '2020-05-06', 'Descending');
  }, []);

  const listEndReached = () => {
    if (state.hasNext) {
      getArticles(state.currentPage + 1, '2020-04-28', '2020-05-06', 'Descending');
    } else {
      setEndReached(true);
    }
  }

  const onItemPress = (index) => {
    console.log('pressed article!');
  };

  const scrollToTop = () => {
    articleListRef.current.scrollToOffset({ animated: true, offset: 0 })
  };

  const renderlistFooter = () => (
    <Layout>
      {endReached ? <Button
        style={styles.endButton}
        size='giant'
        onPress={scrollToTop}>
        scrollToTop
     </Button> : <Layout style={styles.spinnerContent}>
          <Spinner size='large' />
        </Layout>}
    </Layout>
  );


  const renderItemHeader = (article) => (
    <ImageBackground
      style={styles.itemHeader}
      source={article.item.image}
    />
  );

  const renderItemFooter = (article) => (
    <View style={styles.itemFooter}>
      <View style={styles.itemAuthoringContainer}>
        <Text
          category='s2'>
          {article.item.user.email}
        </Text>
        <Text
          appearance='hint'
          category='c1'>
          {article.item.created_date}
        </Text>
      </View>
    </View>
  );

  const renderItem = (article) => (
    <Card
      style={styles.item}
      header={() => renderItemHeader(article)}
      footer={() => renderItemFooter(article)}
      onPress={() => onItemPress(article.uuid)}>
      <Text category='h5'>
        {article.item.title}
      </Text>
      <Text
        style={styles.itemContent}
        appearance='hint'
        category='s1'>
        {article.item.preview}
      </Text>
    </Card>
  );

  return (
    <Layout
      style={styles.container}
      level='2'>
      <List
        ref={articleListRef}
        style={styles.list}
        contentContainerStyle={styles.listContent}
        data={state.articles}
        renderItem={renderItem}
        onEndReached={listEndReached}
        onEndReachedThreshold={0.5}
        ListFooterComponent={renderlistFooter}
      />
    </Layout>

  );
};

const themedStyles = StyleService.create({
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
  popoverContent: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  spinnerContent: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'background-basic-color-2',
  },
  endButton: {
    marginTop: 15,
    marginHorizontal: 16,
  }
});