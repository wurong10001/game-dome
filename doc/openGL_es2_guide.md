# 说明
# 本文针对 Kivy + Buildozer + OpenGL ES 2.0（GLES2）方案。
# 1. Buildozer 关键配置（已在 buildozer.spec 中更新）
# 2. Kivy RenderContext 使用示例（最小三角形）
# 3. 高度图处理、顶点/法线、MVP
# 4. 进阶步骤

# 建议后续实现：
# - 生成网格（双重循环）
# - 加载高度图（numpy + Pillow）
# - 纹理贴图（kivy.graphics.texture）
# - 法线计算（折线）
# - 深度测试（glEnable(GL_DEPTH_TEST) via pyglet/glctypes）
# 注意：已移除 kivy3d 依赖，改用 moderngl + Kivy Canvas 原生 GLES 2.0
