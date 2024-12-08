# 天韵手机账务系统

一个用于手机店管理的全栈应用系统，包含手机入库、销售、回收等功能。

## 技术栈

### 前端
- Vue 3
- Vue Router
- Axios
- Element Plus
- Vite

### 后端
- FastAPI
- SQLite
- SQLAlchemy
- Python-jose (JWT认证)
- Bcrypt (密码加密)

## 主要功能

- 用户认证系统
  - 登录/登出
  - 验证码功能
  - JWT token 认证

- 手机管理
  - 手机入库
  - 采购管理
  - 回收管理
  - IMEI 搜索
  - 库存管理

- 信息广场
  - 手机信息分享
  - 价格查询
  - 信息浏览

## 项目结构

```
tianyu-phone/
├── frontend/                # 前端项目目录
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面组件
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── backend/                # 后端项目目录
    ├── app/
    │   └── routers/       # API路由
    ├── main.py            # 后端入口文件
    └── requirements.txt   # Python依赖
```

## 运行项目

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

## API 端点

- `POST /api/login` - 用户登录
- `GET /api/phones` - 获取手机列表
- `POST /api/phones` - 添加新手机
- `GET /api/phones/search` - 搜索手机
- `POST /api/recycle/add` - 添加回收记录
- `GET /api/info-square` - 获取信息广场数据

## 特性

1. 响应式设计，支持移动端访问
2. 实时验证码功能
3. 完整的认证流程
4. IMEI 编号追踪
5. 多级权限管理
6. 库存实时更新

## 环境要求

- Node.js >= 16
- Python >= 3.8
- SQLite 3

## 开发计划

- [ ] 添加销售统计图表
- [ ] 增加数据导出功能
- [ ] 添加批量导入功能
- [ ] 优化移动端体验
- [ ] 增加更多报表功能

## 参与贡献

1. Fork 项目
2. 创建新的功能分支
3. 提交你的修改
4. 创建 Pull Request

## 许可证

[MIT License](LICENSE)
