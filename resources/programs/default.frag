#version 330
in vec3 v_color;
out vec4 f_color;
void main() {
    // We're not interested in changing the alpha value
    f_color = vec4(v_color, 1.0);
}