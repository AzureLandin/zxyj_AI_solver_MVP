/**
 * AI解题助手 - 前端交互逻辑
 * 前后端完全分离，通过API与后端通信
 */

$(document).ready(function() {
    // 配置
    const API_BASE_URL = 'http://106.54.224.78:5000/api';
    
    // 初始化
    initApp();
    
    // 应用初始化
    function initApp() {
        bindEvents();
        loadConfig();
        console.log('AI解题助手已初始化');
    }
    
    // 绑定事件
    function bindEvents() {
        // 表单提交
        $('#problemForm').on('submit', handleSolveProblem);
        
        // 示例题目点击
        $('.example-item').on('click', function(e) {
            e.preventDefault();
            const exampleText = $(this).text().trim();
            $('#problemInput').val(exampleText);
            $('#problemInput').focus();
        });
        
        // 复制按钮
        $('#copyBtn').on('click', copySolution);
        
        // 清除按钮
        $('#clearBtn').on('click', clearSolution);
        
        // 关于模态框显示时加载配置
        $('#aboutModal').on('show.bs.modal', loadConfig);
    }
    
    // 加载配置信息
    function loadConfig() {
        // 获取当前模型信息
        $.ajax({
            url: `${API_BASE_URL}/models`,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    $('#currentModel').text(response.data.current_model);
                }
            },
            error: function() {
                $('#currentModel').text('未连接');
            }
        });
        
        // 显示API地址
        $('#apiEndpoint').text(API_BASE_URL.replace('/api', ''));
    }
    
    // 处理解题请求
    function handleSolveProblem(e) {
        e.preventDefault();
        
        const problem = $('#problemInput').val().trim();
        
        if (!problem) {
            showError('请输入题目内容');
            $('#problemInput').focus();
            return;
        }
        
        // 显示加载状态
        showLoadingState();
        
        // 调用API
        $.ajax({
            url: `${API_BASE_URL}/solve`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                problem: problem
            }),
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    showSolution(response.data);
                } else {
                    showError(response.error || '获取解答失败');
                }
            },
            error: function(xhr, status, error) {
                let errorMessage = '请求失败：';
                
                if (xhr.status === 0) {
                    errorMessage += '无法连接后端服务，请确保Flask服务器已启动';
                } else if (xhr.status === 400) {
                    errorMessage += '请求参数错误';
                } else if (xhr.status === 500) {
                    errorMessage += '服务器内部错误';
                } else {
                    errorMessage += error || '未知错误';
                }
                
                showError(errorMessage);
            },
            complete: function() {
                // 隐藏加载状态
                $('#solveBtn').prop('disabled', false);
            }
        });
    }
    
    // 显示加载状态
    function showLoadingState() {
        $('#initialState').hide();
        $('#answerContent').hide();
        $('#errorState').hide();
        $('#loadingState').show();
        
        $('#solveBtn').prop('disabled', true);
        $('#solveBtn').html('<i class="fa fa-spinner fa-spin"></i> 解题中...');
    }
    
    // 显示解答
    function showSolution(data) {
        $('#loadingState').hide();
        $('#errorState').hide();
        $('#initialState').hide();
        
        // 填充内容
        $('#problemText').text(data.problem);
        $('#solutionText').text(data.solution);
        
        // 显示答案区域
        $('#answerContent').show().addClass('fade-in');
        
        // 恢复按钮
        $('#solveBtn').html('<i class="fa fa-magic"></i> AI解题');
        $('#solveBtn').prop('disabled', false);
        
        console.log('解答已显示');
    }
    
    // 显示错误信息
    function showError(message) {
        $('#loadingState').hide();
        $('#answerContent').hide();
        $('#initialState').hide();
        
        $('#errorMessage').text(message);
        $('#errorState').show();
        
        // 恢复按钮
        $('#solveBtn').html('<i class="fa fa-magic"></i> AI解题');
        $('#solveBtn').prop('disabled', false);
        
        console.error('错误：', message);
    }
    
    // 复制答案到剪贴板
    function copySolution() {
        const solutionText = $('#solutionText').text();
        
        if (!solutionText) {
            alert('没有答案可复制');
            return;
        }
        
        // 创建临时文本区域
        const $temp = $('<textarea>');
        $('body').append($temp);
        $temp.val(solutionText).select();
        
        try {
            document.execCommand('copy');
            showCopySuccess();
        } catch (err) {
            console.error('复制失败：', err);
            alert('复制失败，请手动复制');
        }
        
        $temp.remove();
    }
    
    // 显示复制成功提示
    function showCopySuccess() {
        const $btn = $('#copyBtn');
        const originalText = $btn.html();
        
        $btn.html('<i class="fa fa-check"></i> 已复制');
        $btn.addClass('btn-success').removeClass('btn-default');
        
        setTimeout(function() {
            $btn.html(originalText);
            $btn.addClass('btn-default').removeClass('btn-success');
        }, 2000);
    }
    
    // 清除答案
    function clearSolution() {
        $('#answerContent').hide();
        $('#errorState').hide();
        $('#initialState').show();
        $('#problemInput').val('').focus();
        
        console.log('答案已清除');
    }
    
    // 显示成功消息
    function showSuccess(message) {
        // 创建临时提示
        const $alert = $(`
            <div class="alert alert-success alert-dismissible fade in" style="position: fixed; top: 80px; right: 20px; z-index: 9999; min-width: 250px;">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <i class="fa fa-check-circle"></i> ${message}
            </div>
        `);
        
        $('body').append($alert);
        
        // 3秒后自动消失
        setTimeout(function() {
            $alert.fadeOut(function() {
                $alert.remove();
            });
        }, 3000);
    }
    
    // 公共函数
    window.App = {
        showSuccess: showSuccess,
        showError: showError,
        clearSolution: clearSolution
    };
});
