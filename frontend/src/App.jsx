import React, { useState, useEffect } from 'react';
import './App.css';
import { useAppContext } from './store';
import { agentApi } from './services/api';

function App() {
  const { state, setAgents, setSelectedAgent, setMessages, addMessage, setLoading, setError } = useAppContext();
  const [inputMessage, setInputMessage] = useState('');
  
  // 获取所有代理
  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      // 实际API调用
      const response = await agentApi.getAllAgents();
      setAgents(response.data);
    } catch (error) {
      console.error('获取代理列表失败:', error);
      setError('获取代理列表失败');
      // 模拟数据
      setAgents([
        { id: '1', name: '贾维斯助手' },
        { id: '2', name: '数据分析员' },
        { id: '3', name: '文档整理员' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 发送消息给代理
  const sendMessage = async () => {
    if (!inputMessage.trim() || !state.selectedAgent || state.loading) return;

    setLoading(true);
    
    try {
      // 添加用户消息到界面
      const userMessage = {
        id: Date.now(),
        role: 'user',
        content: inputMessage,
        timestamp: new Date()
      };
      
      addMessage(userMessage);
      
      // 实际API调用
      // const response = await agentApi.sendMessage(state.selectedAgent.id, {
      //   message: inputMessage
      // });
      
      // 模拟代理回复
      setTimeout(() => {
        const agentMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: `这是来自${state.selectedAgent.name}的回复：${inputMessage}`,
          timestamp: new Date()
        };
        addMessage(agentMessage);
        setLoading(false);
      }, 1000);
      
      setInputMessage('');
    } catch (error) {
      console.error('发送消息失败:', error);
      setError('发送消息失败');
      setLoading(false);
    }
  };

  // 选择代理
  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
    setMessages([]);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>本地贾维斯系统</h1>
        <p>您的智能个人助理</p>
      </header>

      <div className="main-content">
        {/* 代理列表侧边栏 */}
        <aside className="sidebar">
          <h2>智能代理</h2>
          <div className="agent-list">
            {state.agents.map(agent => (
              <div 
                key={agent.id} 
                className={`agent-item ${state.selectedAgent?.id === agent.id ? 'selected' : ''}`}
                onClick={() => handleSelectAgent(agent)}
              >
                {agent.name}
              </div>
            ))}
          </div>
          
          <div className="agent-actions">
            <button className="btn-primary">创建新代理</button>
            <button className="btn-secondary">管理工具</button>
          </div>
        </aside>

        {/* 聊天主界面 */}
        <main className="chat-container">
          {state.selectedAgent ? (
            <>
              <div className="chat-header">
                <h2>与 {state.selectedAgent.name} 对话</h2>
              </div>
              
              <div className="chat-messages">
                {state.messages.map(message => (
                  <div key={message.id} className={`message ${message.role}`}>
                    <div className="message-content">
                      {message.content}
                    </div>
                    <div className="message-time">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                ))}
                {state.loading && (
                  <div className="message assistant">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              <div className="chat-input">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder={`向 ${state.selectedAgent.name} 发送消息...`}
                  disabled={state.loading}
                />
                <button 
                  onClick={sendMessage} 
                  disabled={state.loading || !inputMessage.trim()}
                  className="send-button"
                >
                  发送
                </button>
              </div>
            </>
          ) : (
            <div className="no-agent-selected">
              <h2>欢迎使用本地贾维斯系统</h2>
              <p>请选择一个智能代理开始对话</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;