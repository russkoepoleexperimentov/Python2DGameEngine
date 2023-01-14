#version 330
in vec2 in_vert;
in vec2 in_uv;
in float in_tex;

uniform mat4 projection;

out vec2 v_uv;
out float v_tex;

void main() {
    v_tex = in_tex;
    v_uv = in_uv;
    gl_Position = projection * vec4(in_vert, 0, 1.0);
}