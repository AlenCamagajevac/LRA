import React from 'react';
import {
  Input,
  Layout,
  StyleService,
  useStyleSheet,
  Modal,
  List,
  Spinner,
  Card,
  Text,
  Button
} from '@ui-kitten/components';
import { ImageBackground, View } from 'react-native';
import { SearchIcon } from '../../../assets/icons';
import { FilterModal } from '../../components/filter-modal.component';
import moment from "moment";
import { Context } from '../../context/article.context';

const sortOrderOptions = [
  { text: 'Descending' },
  { text: 'Ascending' }
]

const filterData = {
  toDate: moment().add(1, 'days'),
  fromDate: moment().subtract(7, 'days'),
  sort: sortOrderOptions[0].text
}

export const AllArticlesScreen = (props) => {

  const [query, setQuery] = React.useState('');
  const [filter, setFilter] = React.useState(filterData);
  const [filterModalVisible, setFilterModalVisible] = React.useState(false);
  const [endReached, setEndReached] = React.useState(false);

  const { state, loadArticles, loadMoreArticles } = React.useContext(Context);

  const styles = useStyleSheet(themedStyles);
  const articleListRef = React.useRef()

  React.useEffect(() => {
    loadArticles(filter.fromDate.format('YYYY-MM-DD'), filter.toDate.format('YYYY-MM-DD'), filter.sort, query);
  }, [filter, query]);

  const renderFilterModal = () => {
    return (
      <Layout
        level='3'
        style={styles.modalContainer}>
        <FilterModal
          fromDate={filter.fromDate}
          toDate={filter.toDate}
          sort={filter.sort}
          sortOptions={sortOrderOptions}
          onFilterApply={applyFilter}
        />
      </Layout>
    )
  };

  const applyFilter = (filterData) => {
    toggleFilterModal();
    setEndReached(false);
    setFilter(filterData);
  };

  const toggleFilterModal = () => {
    setFilterModalVisible(!filterModalVisible);
  };

  const onChangeQuery = (query) => {

  };

  const listEndReached = () => {
    if (state.hasNext) {
      loadMoreArticles(state.currentPage + 1, filter.fromDate.format('yyyy-MM-dd'), filter.toDate.format('yyyy-MM-dd'), filter.sort, query);
    } else {
      setEndReached(true);
    }
  }

  const scrollToTop = () => {
    articleListRef.current.scrollToOffset({ animated: true, offset: 0 })
  };

  const renderlistFooter = () => {
    return endReached ? renderScrollToTopButton() : state.articles.length === 0 && !state.hasNext ? renderNoMoreArticlesText() : renderSpinner();
  }

  const renderNoMoreArticlesText = () => (
    <View style={styles.itemFooter}>
      <View style={styles.itemAuthoringContainer}>
        <Text
          category='s2'>
          We have no more articles
        </Text>
        <Text
          appearance='hint'
          category='c1'>
          Try changing filter options
        </Text>
      </View>
    </View>
  );

  const renderSpinner = () => (
    <Layout style={styles.spinnerContent}>
      <Spinner size='large' />
    </Layout>
  )

  const renderScrollToTopButton = () => (
    <Button
      style={styles.endButton}
      size='giant'
      onPress={scrollToTop}>
      scrollToTop
     </Button>
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
    <Layout style={styles.container}>
      <Modal
        backdropStyle={styles.backdrop}
        onBackdropPress={toggleFilterModal}
        visible={filterModalVisible}>
        {renderFilterModal()}
      </Modal>
      <Input
        style={styles.filterInput}
        placeholder='Search'
        value={query}
        icon={SearchIcon}
        onIconPress={toggleFilterModal}
        onChangeText={onChangeQuery}
      />
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
  noMoreArticlesContainer: {
    minHeight: 216,
    paddingHorizontal: 64,
    justifyContent: 'center',
    alignItems: 'center',
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
  },
  filterInput: {
    marginTop: 16,
    marginHorizontal: 8,
  },
  modalContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 300,
    padding: 0,
  },
  backdrop: {
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
});


