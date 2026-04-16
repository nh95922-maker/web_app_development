from flask import Blueprint, render_template, request, redirect, url_for

# 宣告名為 task_bp 的 Blueprint 元件
task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁與所有任務清單 (依照時間和狀態排序)
    此處將渲染: index.html
    """
    pass

@task_bp.route('/tasks/new', methods=['GET'])
def new_task():
    """
    回傳新增任務表單渲染畫面
    此處將渲染: form.html
    """
    pass

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    負責接收 form POST 請求
    將資料進行寫入
    完成後重導向至 index
    """
    pass

@task_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    根據 task_id 提取特定任務，顯示於填答完成的表單上
    此處將渲染: form.html
    """
    pass

@task_bp.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    """
    負責接收對單一 task_id 已經修改過的變更請求
    寫入更新完成後重導向至 index
    """
    pass

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    處理刪除指定 task_id 的刪除行為
    刪除完畢重導向至 index
    """
    pass

@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換指定 task_id 的已完成狀態 0/1 切換
    成功後重導向至 index
    """
    pass
