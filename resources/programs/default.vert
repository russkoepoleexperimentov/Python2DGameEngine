#version 330
in vec2 in_vert;

uniform mat4 projection;

out vec3 v_color;    // Goes to the fragment shader
void main() {
    v_color = vec3(1.0);
    gl_Position = projection * vec4(in_vert, 0, 1.0);
}