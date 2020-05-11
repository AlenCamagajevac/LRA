import React from 'react';
import {
  Input,
  Layout,
  List,
  ListItem,
  StyleService,
  Text,
  useStyleSheet,
} from '@ui-kitten/components';
import { AppRoute } from '../../navigation/app-routes';
import { ProgressBar } from '../../components/progress-bar.component';
import { SearchIcon } from '../../assets/icons';
import { Todo } from '../../data/todo.model';

const allTodos = [
  Todo.mocked0(),
  Todo.mocked1(),
  Todo.mocked2(),
  Todo.mocked0(),
  Todo.mocked1(),
  Todo.mocked2(),
  Todo.mocked0(),
  Todo.mocked1(),
  Todo.mocked2(),
];

export const TodoInProgressScreen = (props) => {

  const [todos, setTodos] = React.useState(allTodos);
  const [query, setQuery] = React.useState('');
  const styles = useStyleSheet(themedStyles);

  const onChangeQuery = (query) => {
    const nextTodos = allTodos.filter((todo) => {
      return todo.title.toLowerCase().includes(query.toLowerCase());
    });

    setTodos(nextTodos);
    setQuery(query);
  };

  const navigateTodoDetails = (todoIndex) => {
    const { [todoIndex]: todo } = todos;
    props.navigation.navigate(AppRoute.TODO_DETAILS, { todo });
  };

  const renderTodo = ({ item }) => (
    <ListItem
      style={styles.item}
      onPress={navigateTodoDetails}>
      <Text category='s1'>
        {item.title}
      </Text>
      <Text
        appearance='hint'
        category='c1'>
        {item.description}
      </Text>
      <ProgressBar
        style={styles.itemProgressBar}
        progress={item.progress}
        text={`${item.progress}%`}
      />
    </ListItem>
  );

  return (
    <Layout style={styles.container}>
      <Input
        style={styles.filterInput}
        placeholder='Search'
        value={query}
        icon={SearchIcon}
        onChangeText={onChangeQuery}
      />
      <List
        style={styles.list}
        data={todos}
        renderItem={renderTodo}
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
  list: {
    flex: 1,
    backgroundColor: 'background-basic-color-1',
  },
  item: {
    flexDirection: 'column',
    alignItems: 'flex-start',
    paddingHorizontal: 12,
  },
  itemProgressBar: {
    width: '50%',
    marginVertical: 12,
  },
});


