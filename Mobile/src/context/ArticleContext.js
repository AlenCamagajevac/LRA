import createDataContext from './CreateDataContext';
import client from '../api/client';

const articleReducer = (state, action) => {
    switch (action.type) {
      case 'get_articles':
        return {
            articles: state.articles.concat(action.payload.items),
            currentPage: action.payload.page,
            hasNext: action.payload.has_next,
            hasPrev: action.payload.has_prev,
            selectedArticleId: state.selectedArticleId  
        };
      case 'get_article_details':
        return state
      default:
        return state;
    }
  };

const getArticles = dispatch => async ( page, from, to, sort ) => {
    try {
        // Send login request   
        const response = await client.get('/api/article', {params: {
            page,
            from,
            to,
            sort
        }});
        // Set new state
        dispatch({ type: 'get_articles', payload: response.data });
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
    { getArticles, getArticleDetails },
    { articles: [], selectedArticleId: null, currentPage: 1, hasPrev: false, hasNext: true }
  );