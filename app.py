from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import io
import zipfile
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 标签模型
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color = db.Column(db.String(20), default='#8A84FF')

# 提示词模型
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.relationship('Tag', secondary='prompt_tag', backref='prompts')

# 提示词与标签的多对多关系
prompt_tag = db.Table('prompt_tag',
    db.Column('prompt_id', db.Integer, db.ForeignKey('prompt.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

with app.app_context():
    db.create_all()
    
    # 初始化标签 - 职场写作者高频使用
    default_tags = [
        {'name': '公文写作', 'color': '#4CAF50'},      # 工作总结、汇报、通知
        {'name': '邮件沟通', 'color': '#2196F3'},      # 商务邮件、跟进邮件
        {'name': '创意文案', 'color': '#FF9800'},      # 营销文案、标题、Slogan
        {'name': '编辑润色', 'color': '#9C27B0'},      # 改写、精简、校对
        {'name': '会议效率', 'color': '#00BCD4'},      # 纪要、议程、跟进
        {'name': '社媒运营', 'color': '#E91E63'},      # 小红书、LinkedIn、朋友圈
        {'name': '报告分析', 'color': '#3F51B5'},      # 数据报告、调研分析
        {'name': '求职简历', 'color': '#FF5722'},      # 简历、求职信、面试
        {'name': '翻译双语', 'color': '#607D8B'},      # 中英互译、本地化
        {'name': '知识整理', 'color': '#8BC34A'},      # 读书笔记、资料提炼
    ]
    
    for tag_data in default_tags:
        if not Tag.query.filter_by(name=tag_data['name']).first():
            tag = Tag(name=tag_data['name'], color=tag_data['color'])
            db.session.add(tag)
    
    # 初始化SEO相关提示词
    seo_prompts = [
        {
            'title': '生成Meta description',
            'content': 'Generate 5 unique meta descriptions, of a maximum of 150 characters, for the following text. The entire conversation and instructions should be provided in Chinese. They should be catchy with a call to action, including the term [主要关键词] in them: [页面内容]',
            'tags': ['SEO']
        },
        {
            'title': '生成常见问答',
            'content': 'Generate a list of 10 frequently asked questions based on the following content: [内容]. The entire conversation and instructions should be provided in Chinese.',
            'tags': ['SEO']
        },
        {
            'title': '生成热门问题',
            'content': 'Generate a list of 10 popular questions related to [关键词], that are relevant for [受众]. The entire conversation and instructions should be provided in Chinese.',
            'tags': ['SEO']
        },
        {
            'title': '文本改写',
            'content': 'Rephrase the following paragraph with Chinese in 5 different ways, to avoid repetition, while keeping its meaning: [修改文本]',
            'tags': ['SEO']
        }
    ]
    
    for prompt_data in seo_prompts:
        if not Prompt.query.filter_by(title=prompt_data['title']).first():
            prompt = Prompt(title=prompt_data['title'], content=prompt_data['content'])
            for tag_name in prompt_data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if tag:
                    prompt.tags.append(tag)
            db.session.add(prompt)
    
    db.session.commit()

@app.route('/')
def index():
    tags = Tag.query.all()
    selected_tag = request.args.get('tags')
    
    if selected_tag:
        tag = Tag.query.filter_by(name=selected_tag).first()
        prompts = tag.prompts if tag else []
    else:
        prompts = Prompt.query.all()
    
    return render_template('index.html', tags=tags, prompts=prompts, selected_tag=selected_tag)

@app.route('/add_tag', methods=['POST'])
def add_tag():
    tag_name = request.form.get('tag_name')
    if tag_name:
        existing_tag = Tag.query.filter_by(name=tag_name).first()
        if not existing_tag:
            import random
            colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#FF5722', '#00BCD4', '#E91E63', '#3F51B5', '#607D8B']
            color = random.choice(colors)
            
            new_tag = Tag(name=tag_name, color=color)
            db.session.add(new_tag)
            db.session.commit()
            return jsonify({'success': True, 'tag': {'id': new_tag.id, 'name': new_tag.name, 'color': new_tag.color}})
        else:
            return jsonify({'success': True, 'tag': {'id': existing_tag.id, 'name': existing_tag.name, 'color': existing_tag.color}})
    return jsonify({'success': False})

@app.route('/delete_tag/<int:tag_id>', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/get_prompt/<int:prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """获取提示词详情"""
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({'success': False, 'error': '提示词不存在'})
    
    return jsonify({
        'success': True,
        'prompt': {
            'id': prompt.id,
            'title': prompt.title,
            'content': prompt.content,
            'tags': [{'id': tag.id, 'name': tag.name, 'color': tag.color} for tag in prompt.tags]
        }
    })

@app.route('/update_prompt/<int:prompt_id>', methods=['POST'])
def update_prompt(prompt_id):
    """更新提示词内容"""
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({'success': False, 'error': '提示词不存在'})
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '无效的请求数据'})
    
    if 'content' in data:
        prompt.content = data['content']
    if 'title' in data:
        prompt.title = data['title']
    
    db.session.commit()
    return jsonify({'success': True, 'message': '保存成功'})

@app.route('/delete_prompt/<int:prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    """删除提示词"""
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({'success': False, 'error': '提示词不存在'})
    
    try:
        db.session.delete(prompt)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/add_prompt', methods=['POST'])
def add_prompt():
    """添加新提示词"""
    title = request.form.get('title')
    content = request.form.get('content')
    tag_names = request.form.getlist('tags')

    if title and content:
        prompt = Prompt(title=title, content=content)

        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                import random
                colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#FF5722', '#00BCD4', '#E91E63', '#3F51B5', '#607D8B']
                color = random.choice(colors)
                tag = Tag(name=tag_name, color=color)
                db.session.add(tag)
            prompt.tags.append(tag)

        db.session.add(prompt)
        db.session.commit()
        return jsonify({'success': True, 'prompt_id': prompt.id})
    return jsonify({'success': False})

@app.route('/get_all_tags', methods=['GET'])
def get_all_tags():
    """获取所有标签"""
    tags = Tag.query.all()
    return jsonify({
        'success': True,
        'tags': [{'id': tag.id, 'name': tag.name, 'color': tag.color} for tag in tags]
    })

@app.route('/update_prompt_tags/<int:prompt_id>', methods=['POST'])
def update_prompt_tags(prompt_id):
    """更新提示词的标签"""
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({'success': False, 'error': '提示词不存在'})
    
    data = request.get_json()
    if not data or 'tag_ids' not in data:
        return jsonify({'success': False, 'error': '无效的请求数据'})
    
    try:
        prompt.tags = []
        for tag_id in data['tag_ids']:
            tag = Tag.query.get(tag_id)
            if tag:
                prompt.tags.append(tag)
        db.session.commit()
        return jsonify({'success': True, 'message': '标签更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export_prompts', methods=['GET'])
def export_prompts():
    """导出提示词为Markdown文件（打包为zip）"""
    try:
        prompts = Prompt.query.all()
        
        if not prompts:
            return jsonify({'success': False, 'error': '没有可导出的提示词'})
        
        # 创建内存中的zip文件
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for prompt in prompts:
                # 生成文件名（移除非法字符）
                safe_title = re.sub(r'[<>:"/\\|?*]', '', prompt.title)[:50]
                filename = f"{safe_title}.md"
                
                # 构建Markdown内容
                content = f"# {prompt.title}\n\n"
                
                # 添加标签信息
                if prompt.tags:
                    tags_str = ', '.join([tag.name for tag in prompt.tags])
                    content += f"**标签**: {tags_str}\n\n"
                
                content += "---\n\n"
                content += prompt.content
                content += "\n"
                
                # 写入zip
                zf.writestr(filename, content.encode('utf-8'))
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'prompts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/import_prompts', methods=['POST'])
def import_prompts():
    """导入Markdown文件作为提示词"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': '未找到文件'})
        
        files = request.files.getlist('files')
        imported_count = 0
        errors = []
        
        for file in files:
            if file and file.filename.endswith('.md'):
                try:
                    # 读取文件内容
                    content = file.read().decode('utf-8')
                    
                    # 解析Markdown
                    lines = content.split('\n')
                    title = ''
                    tags = []
                    body_lines = []
                    in_front_matter = False
                    body_started = False
                    
                    for i, line in enumerate(lines):
                        # 获取标题（第一个#开头的行）
                        if line.startswith('# ') and not title:
                            title = line[2:].strip()
                            continue
                        
                        # 跳过标签行和分隔线
                        if line.startswith('**标签**:') or line.startswith('**标签:**'):
                            tags_str = line.replace('**标签**:', '').replace('**标签:**', '').strip()
                            tags = [t.strip() for t in tags_str.split(',') if t.strip()]
                            continue
                        
                        if line.strip() == '---':
                            if not body_started:
                                body_started = True
                                continue
                        
                        if body_started or (title and i > 0 and not line.startswith('**标签')):
                            body_lines.append(line)
                    
                    # 如果没有找到标题，使用文件名
                    if not title:
                        title = file.filename.replace('.md', '')
                    
                    # 如果没有找到正文，使用全部内容
                    if not body_lines:
                        body_lines = lines[1:] if title else lines
                    
                    body = '\n'.join(body_lines).strip()
                    
                    if not body:
                        body = content
                    
                    # 创建提示词
                    prompt = Prompt(title=title, content=body)
                    
                    # 添加标签
                    for tag_name in tags:
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if not tag:
                            import random
                            colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#FF5722', '#00BCD4', '#E91E63', '#3F51B5', '#607D8B']
                            tag = Tag(name=tag_name, color=random.choice(colors))
                            db.session.add(tag)
                        prompt.tags.append(tag)
                    
                    db.session.add(prompt)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f'{file.filename}: {str(e)}')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'imported': imported_count,
            'errors': errors
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/extract_variables', methods=['POST'])
def extract_variables():
    """从提示词中提取变量占位符"""
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'success': False, 'error': '缺少内容'})

        content = data['content']
        # 匹配 {{变量名}} 格式
        variables = re.findall(r'\{\{(.*?)\}\}', content)
        # 去重并保持顺序
        unique_vars = list(dict.fromkeys(variables))

        return jsonify({
            'success': True,
            'variables': unique_vars
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/apply_variables', methods=['POST'])
def apply_variables():
    """应用变量值替换占位符"""
    try:
        data = request.get_json()
        if not data or 'content' not in data or 'values' not in data:
            return jsonify({'success': False, 'error': '缺少必要参数'})

        content = data['content']
        values = data['values']

        # 替换所有 {{变量名}} 为对应值
        for var_name, var_value in values.items():
            placeholder = '{{' + var_name + '}}'
            content = content.replace(placeholder, str(var_value))

        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
