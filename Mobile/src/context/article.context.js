import createDataContext from './create-data-context';
import client from '../api/client';

const articleReducer = (state, action) => {
  switch (action.type) {
    case 'load_articles':
      return {
        articles: action.payload.items,
        currentPage: action.payload.page,
        hasNext: action.payload.has_next,
        hasPrev: action.payload.has_prev,
        selectedArticleId: state.selectedArticleId
      };
    case 'load_more_articles':
      return {
        articles: state.articles.concat(action.payload.items),
        currentPage: action.payload.page,
        hasNext: action.payload.has_next,
        hasPrev: action.payload.has_prev,
        selectedArticleId: state.selectedArticleId
      };
    case 'clear_articles':
      return {...state, articles: [], hasNext: true}
    case 'get_article_details':
      return state
    default:
      return state;
  }
};

const loadArticles = dispatch => async (from, to, sort, query) => {
  try {
    console.log(from, to, sort, query);
    // Clear existing articles
    dispatch({ type: 'clear_articles'});

    // Send login request   
    const response = await client.get('/api/article', {
      params: {
        from,
        to,
        sort,
        query
      }
    });
    // Set new state
    dispatch({ type: 'load_articles', payload: response.data });
  } catch (err) {
    console.log(err.response);
    dispatch({
      type: 'add_error',
      payload: 'Something went wrong with sign in'
    });
  }
};

const loadMoreArticles = dispatch => async (page, from, to, sort, query) => {
  try {
    // Send login request   
    const response = await client.get('/api/article', {
      params: {
        page,
        from,
        to,
        sort,
        query
      }
    });
    // Set new state
    dispatch({ type: 'load_more_articles', payload: response.data });
  } catch (err) {
    console.log(err.response);
    dispatch({
      type: 'add_error',
      payload: 'Something went wrong with sign in'
    });
  }
};

const getArticleDetails = dispatch => {

}

export const { Context, Provider } = createDataContext(
  articleReducer,
  { loadArticles, loadMoreArticles, getArticleDetails },
  { articles: [], selectedArticleId: null, currentPage: 1, hasPrev: false, hasNext: true }
);