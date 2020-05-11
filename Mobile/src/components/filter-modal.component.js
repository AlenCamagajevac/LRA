import React from 'react';
import {
  Button,
  Text,
  useStyleSheet,
  StyleService,
  Datepicker,
  Select
} from '@ui-kitten/components';
import { CalendarIcon } from '../../assets/icons';
import { View } from 'react-native';
import moment from 'moment';

export const FilterModal = ({ fromDate, toDate, sort, sortOptions, onFilterApply }) => {

  const styles = useStyleSheet(themedStyles);

  const [fromDateFilter, setFromDateFilter] = React.useState(fromDate);
  const [toDateFilter, setToDateFilter] = React.useState(toDate);
  const [sortFilter, setSortFilter] = React.useState(sortOptions[0].text);

  return (
    <View style={themedStyles.formContainer}>
      <View style={styles.headerContainer}>
        <Text
          style={styles.filterLabel}
          category='s1'
          appearance='hint'>
          Please select filters
        </Text>
      </View>
      <Datepicker
        label='From date'
        placeholder='From date'
        onSelect={date => setFromDateFilter(moment(date))}
        date={new Date(fromDateFilter.format())}
        icon={CalendarIcon}
      />
      <Datepicker
        label='To date'
        placeholder='To date'
        onSelect={date => setToDateFilter(moment(date))}
        date={new Date(toDateFilter.format())}
        icon={CalendarIcon}
      />
      <Select
        placeholder={sortFilter}
        label='Sort Order'
        data={sortOptions}
        selectedOption={sortOptions[0].text}
        onSelect={(select) => setSortFilter(select.text)}
        textStyle={themedStyles.selectText}
      />
      <Button
        style={styles.filterButton}
        onPress={() => onFilterApply({ fromDateFilter, toDateFilter, sortFilter })}
        appearance='ghost'
        status='basic'>
        Apply filter
      </Button>
    </View>
  );
}

const themedStyles = StyleService.create({
  formContainer: {
    marginTop: 0,
    paddingHorizontal: 0,
    backgroundColor: 'background-basic-color-1'
  },
  headerContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: 70,
    minWidth: 200,
    backgroundColor: 'background-basic-color-3',
  },
  filterButton: {
    marginVertical: 15,
    marginHorizontal: 16,
  },
});