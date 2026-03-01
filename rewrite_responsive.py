import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ================= 查找 </style> 的位置，并插入媒体查询 =================
responsive_css = """
  /* ================= 移动端适配 (Responsive Design) ================= */
  @media (max-width: 1024px) {
    .year-stats {
      grid-template-columns: repeat(3, 1fr);
    }
    .month-stat-grid {
      grid-template-columns: repeat(4, 1fr);
    }
    .cards {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 768px) {
    body {
      padding: 10px;
    }
    .container {
      padding: 16px;
      border-radius: 12px;
    }
    h1 {
      font-size: 20px;
    }
    .year-stats {
      grid-template-columns: repeat(2, 1fr);
    }
    .month-stat-grid {
      grid-template-columns: repeat(3, 1fr);
    }
    .top-charts {
      flex-direction: column;
    }
    .chart-box, .cards {
      width: 100%;
      min-width: unset;
    }
    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .toolbar button, .toolbar select, .toolbar input {
      flex: 1 1 45%; /* 让按钮排成两列 */
    }
    .toolbar .search {
      flex: 1 1 100%; /* 搜索框占满一行 */
    }
    
    /* 中等屏幕：取消区域列和部分列的冻结，仅保留门店名称和锁定框 */
    .main-table th:nth-child(3), .main-table td:nth-child(3){
      position: static;
      box-shadow: none;
    }
  }

  @media (max-width: 480px) {
    .year-stats {
      grid-template-columns: 1fr;
    }
    .month-stat-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    .cards {
      grid-template-columns: 1fr;
    }
    .toolbar button, .toolbar select {
      flex: 1 1 100%; /* 极小屏幕下完全单列排布 */
    }
    
    /* 极小屏幕：取消所有除 Checkbox 外的冻结列，保证有足够空间浏览核心数据 */
    .main-table th:nth-child(2), .main-table td:nth-child(2){
      position: static;
      box-shadow: none;
    }
  }
</style>
"""

content = content.replace("</style>", responsive_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Responsive script completed.")
