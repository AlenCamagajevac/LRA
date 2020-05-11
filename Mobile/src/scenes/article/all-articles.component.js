import React from 'react';
import {
  Input,
  Layout,
  StyleService,
  useStyleSheet,
  Modal
} from '@ui-kitten/components';
import { SearchIcon } from '../../../assets/icons';
import { FilterModal } from '../../components/filter-modal.component';
import moment from "moment";

const sortOrderOptions = [
  { text: 'Ascending' },
  { text: 'Descending' }
]

const filterData = {
  toDate: moment().add(1, 'days'),
  fromDate:  moment().subtract(7, 'days'),
  sort: sortOrderOptions[0].text
}

export const AllArticlesScreen = (props) => {

  const [query, setQuery] = React.useState('');
  const [filter, setFilter] = React.useState(filterData);
  const [filterModalVisible, setFilterModalVisible] = React.useState(false);
  const styles = useStyleSheet(themedStyles);

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
  )}

  const applyFilter = (filterData) => {
    console.log(filterData);
    toggleFilterModal();
  }

  const toggleFilterModal = () => {
    setFilterModalVisible(!filterModalVisible);
  };

  const onChangeQuery = (query) => {
    
  };


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
    </Layout>
  );
};

const themedStyles = StyleService.create({
  container: {
    flex: 1,
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


