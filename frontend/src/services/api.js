import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    const token = localStorage.getItem('letta_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权错误
      localStorage.removeItem('letta_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 代理相关API
export const agentApi = {
  // 获取所有代理
  getAllAgents: () => apiClient.get('/v1/agents'),
  
  // 创建代理
  createAgent: (data) => apiClient.post('/v1/agents', data),
  
  // 获取代理详情
  getAgent: (agentId) => apiClient.get(`/v1/agents/${agentId}`),
  
  // 更新代理
  updateAgent: (agentId, data) => apiClient.put(`/v1/agents/${agentId}`, data),
  
  // 删除代理
  deleteAgent: (agentId) => apiClient.delete(`/v1/agents/${agentId}`),
  
  // 向代理发送消息
  sendMessage: (agentId, data) => apiClient.post(`/v1/agents/${agentId}/messages`, data),
  
  // 获取代理消息历史
  getMessages: (agentId, limit = 50) => apiClient.get(`/v1/agents/${agentId}/messages?limit=${limit}`),
};

// 工具相关API
export const toolApi = {
  // 获取所有工具
  getAllTools: () => apiClient.get('/v1/tools'),
  
  // 获取MCP工具
  getMcpTools: (serverName) => apiClient.get(`/v1/tools/mcp/servers/${serverName}/tools`),
  
  // 添加MCP服务器
  addMcpServer: (data) => apiClient.post('/v1/tools/mcp/servers', data),
};

// 用户相关API
export const userApi = {
  // 获取当前用户
  getCurrentUser: () => apiClient.get('/v1/users/me'),
};

// 导出axios实例以供直接使用
export default apiClient;