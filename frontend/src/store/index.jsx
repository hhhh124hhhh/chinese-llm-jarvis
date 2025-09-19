import { createContext, useContext, useReducer } from 'react';

// 初始状态
const initialState = {
  agents: [],
  selectedAgent: null,
  messages: [],
  loading: false,
  error: null,
};

// Action types
const ACTIONS = {
  SET_AGENTS: 'SET_AGENTS',
  SET_SELECTED_AGENT: 'SET_SELECTED_AGENT',
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
};

// Reducer
const appReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_AGENTS:
      return { ...state, agents: action.payload };
    
    case ACTIONS.SET_SELECTED_AGENT:
      return { ...state, selectedAgent: action.payload };
    
    case ACTIONS.SET_MESSAGES:
      return { ...state, messages: action.payload };
    
    case ACTIONS.ADD_MESSAGE:
      return { ...state, messages: [...state.messages, action.payload] };
    
    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };
    
    case ACTIONS.SET_ERROR:
      return { ...state, error: action.payload };
    
    default:
      return state;
  }
};

// Context
const AppContext = createContext();

// Provider组件
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Action creators
  const setAgents = (agents) => {
    dispatch({ type: ACTIONS.SET_AGENTS, payload: agents });
  };

  const setSelectedAgent = (agent) => {
    dispatch({ type: ACTIONS.SET_SELECTED_AGENT, payload: agent });
  };

  const setMessages = (messages) => {
    dispatch({ type: ACTIONS.SET_MESSAGES, payload: messages });
  };

  const addMessage = (message) => {
    dispatch({ type: ACTIONS.ADD_MESSAGE, payload: message });
  };

  const setLoading = (loading) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: loading });
  };

  const setError = (error) => {
    dispatch({ type: ACTIONS.SET_ERROR, payload: error });
  };

  const value = {
    state,
    setAgents,
    setSelectedAgent,
    setMessages,
    addMessage,
    setLoading,
    setError,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// 自定义hook
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};