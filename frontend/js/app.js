/**
 * AI解题助手 - 现代化前端交互逻辑
 * 参考作业帮、豆包爱学等流行应用
 */

$(document).ready(function() {
    // API配置
    const API_BASE_URL = 'http://localhost:5000/api';
    
    // 全局变量
    let selectedImage = null;
    let currentMode = null; // 'camera' 或 'text'
    let searchHistory = []; // 搜题记录
    
    // 初始化应用
    initApp();
    
    function initApp() {
        bindEvents();
        loadConfig();
        loadSearchHistory();
        console.log('AI解题助手已初始化');
    }
    
    // 绑定事件
    function bindEvents() {
        // 功能卡片点击
        $('#cameraCard').on('click', () => openInputMode('camera'));
        $('#textCard').on('click', () => openInputMode('text'));

        // 全局返回按钮
        $('#globalBackBtn').on('click', function() {
            if ($('#resultSection').is(':visible')) {
                closeResult();
            } else if ($('#inputSection').is(':visible')) {
                closeInputMode();
            }
        });

        // 图片上传相关
        $('#uploadPreview').on('click', () => $('#imageInput').click());
        $('#imageInput').on('change', handleImageSelect);
        $('#submitImage').on('click', submitImageProblem);
        $('#cancelImage').on('click', closeInputMode);
        
        // 文字输入相关
        $('#submitText').on('click', submitTextProblem);
        $('#cancelText').on('click', closeInputMode);
        
        // 结果操作（已改为全局返回按钮）
        $('#copyBtn').on('click', copySolution);
        $('#newQuestionBtn').on('click', resetToHome);
        
        // 拖拽上传
        setupDragAndDrop();

        // 模态框加载配置
        $('#aboutModal').on('show.bs.modal', loadConfig);

        // 搜题记录相关
        $('#historyBtn').on('click', openHistory);
        $('#closeHistory').on('click', closeHistory);
        $('#historyBackdrop').on('click', closeHistory);
        $('#clearHistory').on('click', clearHistory);
    }
    
    // 打开输入模式
    function openInputMode(mode) {
        currentMode = mode;

        // 隐藏hero区域
        $('.hero-section').slideUp(300);

        // 添加居中模式类
        $('.main-wrapper').addClass('has-input');

        // 显示全局返回按钮
        $('#globalBackBtn').fadeIn(300);

        // 显示输入区域
        setTimeout(() => {
            $('#inputSection').fadeIn(300);

            if (mode === 'camera') {
                $('#uploadArea').fadeIn(300);
                $('#textInputArea').hide();
            } else {
                $('#textInputArea').fadeIn(300);
                $('#uploadArea').hide();
            }
        }, 300);
    }
    
    // 关闭输入模式
    function closeInputMode() {
        // 清理数据
        selectedImage = null;
        $('#imageInput').val('');
        $('#previewImage').hide();
        $('.upload-placeholder').show();
        $('#uploadActions').hide();
        $('#problemInput').val('');

        // 移除居中模式类
        $('.main-wrapper').removeClass('has-input');

        // 隐藏全局返回按钮
        $('#globalBackBtn').fadeOut(300);

        // 隐藏输入区域
        $('#inputSection').fadeOut(300);
        $('#uploadArea').hide();
        $('#textInputArea').hide();

        // 显示hero区域
        setTimeout(() => {
            $('.hero-section').slideDown(300);
        }, 300);
    }
    
    // 处理图片选择
    function handleImageSelect(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        // 验证文件类型
        if (!file.type.match('image.*')) {
            showToast('请选择图片文件（JPG、PNG）');
            return;
        }
        
        // 验证文件大小
        if (file.size > 10 * 1024 * 1024) {
            showToast('图片大小不能超过10MB');
            return;
        }
        
        selectedImage = file;
        
        // 显示预览
        const reader = new FileReader();
        reader.onload = function(e) {
            $('#previewImage').attr('src', e.target.result).show();
            $('.upload-placeholder').hide();
            $('#uploadActions').fadeIn(300);
        };
        reader.readAsDataURL(file);
    }
    
    // 设置拖拽上传
    function setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadPreview');
        
        if (!uploadArea) return;
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            $(uploadArea).addClass('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            $(uploadArea).removeClass('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            $(uploadArea).removeClass('drag-over');
            
            const file = e.dataTransfer.files[0];
            if (file && file.type.match('image.*')) {
                $('#imageInput')[0].files = e.dataTransfer.files;
                handleImageSelect({ target: { files: [file] } });
            }
        });
    }
    
    // 提交图片题目
    function submitImageProblem() {
        if (!selectedImage) {
            showToast('请选择题目图片');
            return;
        }
        
        // 显示加载动画
        showLoading();
        
        // 准备表单数据
        const formData = new FormData();
        formData.append('image', selectedImage);
        
        // 调用API
        $.ajax({
            url: `${API_BASE_URL}/solve-image`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                hideLoading();
                if (response.success) {
                    // 添加到搜题记录
                    addSearchHistory({
                        type: 'image',
                        problem: '图片题目',
                        solution: response.data.solution,
                        timestamp: new Date().getTime()
                    });
                    showResult(response.data);
                } else {
                    showToast(response.error || '获取解答失败');
                }
            },
            error: (xhr) => {
                hideLoading();
                handleAPIError(xhr);
            }
        });
    }

    // 提交文字题目
    function submitTextProblem() {
        const problem = $('#problemInput').val().trim();
        
        if (!problem) {
            showToast('请输入题目内容');
            return;
        }
        
        // 显示加载动画
        showLoading();
        
        // 调用API
        $.ajax({
            url: `${API_BASE_URL}/solve`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ problem }),
            success: (response) => {
                hideLoading();
                if (response.success) {
                    // 添加到搜题记录
                    addSearchHistory({
                        type: 'text',
                        problem: problem,
                        solution: response.data.solution,
                        timestamp: new Date().getTime()
                    });
                    showResult(response.data);
                } else {
                    showToast(response.error || '获取解答失败');
                }
            },
            error: (xhr) => {
                hideLoading();
                handleAPIError(xhr);
            }
        });
    }

    // 显示结果
    function showResult(data) {
        // 隐藏输入区域
        $('#inputSection').fadeOut(300);

        // 确保全局返回按钮显示
        $('#globalBackBtn').fadeIn(300);

        setTimeout(() => {
            // 填充题目
            $('#problemText').text(data.problem);

            // 渲染Markdown
            if (typeof marked !== 'undefined') {
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    highlight: (code, lang) => {
                        if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {
                            try {
                                return hljs.highlight(code, { language: lang }).value;
                            } catch (err) {}
                        }
                        return code;
                    }
                });

                let renderedHtml = marked.parse(data.solution);
                
                // 高亮最终答案
                renderedHtml = highlightFinalAnswer(renderedHtml);
                
                $('#solutionText').html(renderedHtml);

                // 应用代码高亮
                if (typeof hljs !== 'undefined') {
                    $('#solutionText pre code').each((i, block) => {
                        hljs.highlightElement(block);
                    });
                }
            } else {
                $('#solutionText').text(data.solution);
            }

            // 显示结果区域
            $('#resultSection').fadeIn(300);
        }, 300);
    }
    
    // 关闭结果
    function closeResult() {
        $('#resultSection').fadeOut(300);
        // 移除居中模式类
        $('.main-wrapper').removeClass('has-input');
        // 隐藏全局返回按钮
        $('#globalBackBtn').fadeOut(300);
        setTimeout(() => {
            $('.hero-section').slideDown(300);
        }, 300);
    }
    
    // 重置到首页
    function resetToHome() {
        closeResult();
        closeInputMode();
    }
    
    // 复制答案
    function copySolution() {
        const text = $('#solutionText').text();
        
        if (!text) {
            showToast('没有答案可复制');
            return;
        }
        
        // 创建临时文本区域
        const $temp = $('<textarea>');
        $('body').append($temp);
        $temp.val(text).select();
        
        try {
            document.execCommand('copy');
            showToast('已复制到剪贴板', 'success');
        } catch (err) {
            showToast('复制失败，请手动复制');
        }
        
        $temp.remove();
    }
    
    // 显示加载动画
    function showLoading() {
        $('#loadingOverlay').fadeIn(300);
    }
    
    // 隐藏加载动画
    function hideLoading() {
        $('#loadingOverlay').fadeOut(300);
    }
    
    // 显示提示消息
    function showToast(message, type = 'error') {
        // 创建toast元素
        const toast = $(`
            <div class="toast-message ${type}">
                <i class="fa ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `);
        
        // 添加样式
        toast.css({
            position: 'fixed',
            top: '80px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: type === 'success' ? '#10b981' : '#ef4444',
            color: 'white',
            padding: '15px 30px',
            borderRadius: '12px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
            zIndex: 3000,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '16px',
            fontWeight: '600',
            animation: 'fadeInDown 0.5s ease'
        });
        
        $('body').append(toast);
        
        // 3秒后消失
        setTimeout(() => {
            toast.fadeOut(300, () => toast.remove());
        }, 3000);
    }
    
    // 处理API错误
    function handleAPIError(xhr) {
        let message = '请求失败：';
        
        if (xhr.status === 0) {
            message += '无法连接服务器';
        } else if (xhr.status === 400) {
            message += '请求参数错误';
        } else if (xhr.status === 500) {
            message += '服务器错误';
        } else {
            message += '未知错误';
        }
        
        showToast(message);
    }
    
    // 高亮最终答案
    function highlightFinalAnswer(html) {
        let highlighted = html;

        // 处理最终答案段落 - 移除内容中的"最终答案："避免重复
        highlighted = highlighted.replace(/<p[^>]*>(最终答案[：:]\s*)(.*?)<\/p>/gi, function(_match, _prefix, content) {
            return '<div class="final-answer-box"><p>' + content + '</p></div>';
        });

        // 处理"答案为/是/结论"格式 - 同样移除前缀
        highlighted = highlighted.replace(/<p[^>]*>((?:答案为|答案是|最终结论)[：:]\s*)(.*?)<\/p>/gi, function(match, _prefix, content) {
            // 避免重复包装
            if (match.includes('final-answer-box')) return match;
            return '<div class="final-answer-box"><p>' + content + '</p></div>';
        });

        // 高亮答案选项 (A/B/C/D)
        highlighted = highlighted.replace(/([（\(]\s*)([A-D])(\s*[）\)])/g,
            '$1<span class="answer-option">$2</span>$3');

        return highlighted;
    }
    
    // 加载配置
    function loadConfig() {
        $.ajax({
            url: `${API_BASE_URL}/models`,
            method: 'GET',
            success: (response) => {
                if (response.success) {
                    const models = response.data;
                    $('#currentModel').text(models.text_model?.current || '未连接');
                }
            },
            error: () => {
                $('#currentModel').text('未连接');
            }
        });
    }

    // ==================== 搜题记录功能 ====================

    // 加载搜题记录
    function loadSearchHistory() {
        const saved = localStorage.getItem('searchHistory');
        if (saved) {
            try {
                searchHistory = JSON.parse(saved);
            } catch (e) {
                searchHistory = [];
            }
        }
    }

    // 保存搜题记录
    function saveSearchHistory() {
        localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
    }

    // 添加搜题记录
    function addSearchHistory(record) {
        // 限制最多保存50条记录
        if (searchHistory.length >= 50) {
            searchHistory = searchHistory.slice(-49);
        }
        searchHistory.push(record);
        saveSearchHistory();
    }

    // 打开搜题记录
    function openHistory() {
        $('#historyOverlay').addClass('active');
        renderHistoryList();
    }

    // 关闭搜题记录
    function closeHistory() {
        $('#historyOverlay').removeClass('active');
    }

    // 渲染搜题记录列表
    function renderHistoryList() {
        const $content = $('#historyContent');

        if (searchHistory.length === 0) {
            $content.html(`
                <div class="history-empty">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width:48px;height:48px;stroke:#ccc;">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    <p>暂无搜题记录</p>
                </div>
            `);
            return;
        }

        // 按时间倒序排列
        const sortedHistory = [...searchHistory].reverse();

        let html = '';
        sortedHistory.forEach((item, index) => {
            const timeStr = formatTimestamp(item.timestamp);
            const isCamera = item.type === 'image';

            html += `
                <div class="history-item" data-index="${searchHistory.length - 1 - index}">
                    <div class="history-item-header">
                        <span class="history-item-type ${item.type}">
                            ${isCamera ? `
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
                                    <circle cx="12" cy="13" r="4"/>
                                </svg>
                                拍照搜题
                            ` : `
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="2" y="6" width="20" height="12" rx="2"/>
                                    <path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01"/>
                                    <path d="M6 14h12"/>
                                </svg>
                                文字搜题
                            `}
                        </span>
                        <span class="history-item-time">${timeStr}</span>
                    </div>
                    <div class="history-item-content ${isCamera ? 'history-item-content-image' : ''}">
                        ${isCamera ? '图片题目 - 点击查看详情' : item.problem}
                    </div>
                </div>
            `;
        });

        $content.html(html);

        // 绑定点击事件，查看历史记录详情
        $('.history-item').on('click', function() {
            const index = $(this).data('index');
            viewHistoryItem(index);
        });
    }

    // 查看历史记录详情
    function viewHistoryItem(index) {
        const item = searchHistory[index];
        if (!item) return;

        // 关闭记录侧边栏
        closeHistory();

        // 显示历史记录的解答
        const data = {
            problem: item.problem,
            solution: item.solution
        };

        // 隐藏hero区域和输入区域
        $('.hero-section').slideUp(300);
        $('#inputSection').fadeOut(300);
        $('.main-wrapper').addClass('has-input');

        setTimeout(() => {
            // 填充解答内容
            if (typeof marked !== 'undefined') {
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    highlight: (code, lang) => {
                        if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {
                            try {
                                return hljs.highlight(code, { language: lang }).value;
                            } catch (err) {}
                        }
                        return code;
                    }
                });

                let renderedHtml = marked.parse(item.solution);
                renderedHtml = highlightFinalAnswer(renderedHtml);
                $('#solutionText').html(renderedHtml);

                if (typeof hljs !== 'undefined') {
                    $('#solutionText pre code').each((i, block) => {
                        hljs.highlightElement(block);
                    });
                }
            } else {
                $('#solutionText').text(item.solution);
            }

            $('#resultSection').fadeIn(300);
        }, 300);
    }

    // 清空搜题记录
    function clearHistory() {
        if (!confirm('确定要清空所有搜题记录吗？')) {
            return;
        }
        searchHistory = [];
        saveSearchHistory();
        renderHistoryList();
        showToast('搜题记录已清空', 'success');
    }

    // 格式化时间戳
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        // 小于1分钟
        if (diff < 60000) {
            return '刚刚';
        }

        // 小于1小时
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes}分钟前`;
        }

        // 小于24小时
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours}小时前`;
        }

        // 小于7天
        if (diff < 604800000) {
            const days = Math.floor(diff / 86400000);
            return `${days}天前`;
        }

        // 超过7天，显示具体日期
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hour = date.getHours().toString().padStart(2, '0');
        const minute = date.getMinutes().toString().padStart(2, '0');

        return `${month}月${day}日 ${hour}:${minute}`;
    }
});
